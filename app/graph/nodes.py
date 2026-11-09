"""Graph nodes. LLM-backed steps are stubbed with simple rules for now."""

from datetime import date

from langgraph.types import interrupt

from app.domain import DocumentType, ServiceType, TicketStatus
from app.graph.state import TicketState
from app.integrations.channels import InsurerChannel, InsurerRequest
from app.services.documents import ExtractedDocument, check_documents

_KEYWORDS: list[tuple[ServiceType, tuple[str, ...]]] = [
    (ServiceType.UAE_EXTENSION, ("uae", "emirates", "dubai", "الإمارات", "الامارات", "دبي")),
    (ServiceType.OWNERSHIP_TRANSFER, ("transfer", "sold", "نقل", "بعت")),
    (ServiceType.ADD_DRIVER, ("add driver", "سائق")),
    (ServiceType.CANCELLATION, ("cancel", "refund", "إلغاء", "الغاء")),
    (ServiceType.POLICY_EXTENSION, ("extend", "extension", "تمديد", "أمدد", "امدد")),
]


def classify(state: TicketState) -> TicketState:
    # TODO(brain): replace with an LLM call using structured output.
    text = state.get("customer_message", "").lower()
    for service, words in _KEYWORDS:
        if any(word in text for word in words):
            return {"service": service.value, "status": TicketStatus.NEW.value}
    return {"service": ServiceType.UNKNOWN.value, "status": TicketStatus.ESCALATED.value}


def _to_document(raw: dict) -> ExtractedDocument:
    expiry = raw.get("expiry")
    return ExtractedDocument(
        doc_type=DocumentType(raw["doc_type"]),
        confidence=raw["confidence"],
        name=raw.get("name"),
        expiry=date.fromisoformat(expiry) if expiry else None,
        plate=raw.get("plate"),
    )


def make_check_documents(today_fn=date.today):
    def check_docs(state: TicketState) -> TicketState:
        issues = check_documents(
            ServiceType(state["service"]),
            [_to_document(d) for d in state.get("documents", [])],
            policy_plate=state.get("policy_plate"),
            today=today_fn(),
        )
        return {"issues": [{"doc_type": i.doc_type.value, "reason": i.reason} for i in issues]}

    return check_docs


def request_documents(state: TicketState) -> TicketState:
    # TODO(brain): let the LLM write a friendly message in the customer's language.
    lines = [f"- {i['doc_type']}: {i['reason']}" for i in state["issues"]]
    message = "We need the following before we can continue:\n" + "\n".join(lines)
    return {
        "status": TicketStatus.AWAITING_DOCUMENTS.value,
        "outbox": [*state.get("outbox", []), message],
    }


def draft_request(state: TicketState) -> TicketState:
    # TODO(brain): draft with the LLM, using RAG for the insurer's own format.
    draft = (
        f"Service: {state['service']}\n"
        f"Ticket: {state['ticket_id']}\n"
        f"Documents: {len(state.get('documents', []))} attached"
    )
    return {"draft": draft, "status": TicketStatus.IN_REVIEW.value}


def staff_approval(state: TicketState) -> TicketState:
    """Gate 1: nothing reaches the insurer without a staff decision."""
    decision = interrupt({"gate": "before_insurer", "draft": state["draft"]})
    if decision.get("approved"):
        return {"draft": decision.get("draft", state["draft"])}
    return {"status": TicketStatus.REJECTED.value, "review_note": decision.get("note", "")}


def make_send_to_insurer(channel: InsurerChannel):
    def send_to_insurer(state: TicketState) -> TicketState:
        receipt = channel.submit(
            InsurerRequest(
                ticket_id=state["ticket_id"],
                insurer_id=state.get("insurer_id", ""),
                service=state["service"],
                body=state["draft"],
            )
        )
        return {"reference": receipt.reference, "status": TicketStatus.AWAITING_INSURER.value}

    return send_to_insurer
