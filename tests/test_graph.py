from datetime import date

from langgraph.types import Command

from app.graph.graph import build_graph
from app.integrations.channels import FakeChannel

TODAY = date(2026, 11, 9)

TRANSFER_DOCS = [
    {"doc_type": "registration", "confidence": 0.95, "expiry": "2027-05-01", "plate": "12345 RB"},
    {"doc_type": "id_card", "confidence": 0.93, "expiry": "2029-01-01"},
]
LICENCE = {"doc_type": "driving_licence", "confidence": 0.9, "expiry": "2028-03-01"}


def run(graph, ticket_id, payload):
    config = {"configurable": {"thread_id": ticket_id}}
    return graph.invoke(payload, config), config


def ticket(ticket_id, message, documents):
    return {
        "ticket_id": ticket_id,
        "insurer_id": "insurer-a",
        "customer_message": message,
        "policy_plate": "12345 RB",
        "documents": documents,
    }


def test_missing_document_asks_customer_and_stops():
    channel = FakeChannel()
    graph = build_graph(channel, today_fn=lambda: TODAY)

    result, _ = run(graph, "T-1", ticket("T-1", "I sold my car, transfer please", TRANSFER_DOCS))

    assert result["service"] == "ownership_transfer"
    assert result["status"] == "awaiting_documents"
    assert "driving_licence" in result["outbox"][-1]
    assert channel.sent == []


def test_complete_ticket_waits_for_staff_then_sends():
    channel = FakeChannel()
    graph = build_graph(channel, today_fn=lambda: TODAY)
    docs = [*TRANSFER_DOCS, LICENCE]

    result, config = run(graph, "T-2", ticket("T-2", "بعت سيارتي وأبغى أنقل التأمين", docs))

    assert result["status"] == "in_review"
    assert "__interrupt__" in result
    assert channel.sent == [], "nothing may reach the insurer before approval"

    result = graph.invoke(Command(resume={"approved": True}), config)

    assert result["status"] == "awaiting_insurer"
    assert result["reference"] == "FAKE-1"
    assert len(channel.sent) == 1


def test_rejected_ticket_is_not_sent():
    channel = FakeChannel()
    graph = build_graph(channel, today_fn=lambda: TODAY)
    docs = [*TRANSFER_DOCS, LICENCE]

    _, config = run(graph, "T-3", ticket("T-3", "transfer to the buyer", docs))
    result = graph.invoke(Command(resume={"approved": False, "note": "wrong policy"}), config)

    assert result["status"] == "rejected"
    assert result["review_note"] == "wrong policy"
    assert channel.sent == []


def test_unrecognised_request_is_escalated():
    graph = build_graph(FakeChannel(), today_fn=lambda: TODAY)
    result, _ = run(graph, "T-4", ticket("T-4", "hello?", []))
    assert result["status"] == "escalated"
