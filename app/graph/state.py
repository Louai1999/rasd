from typing import TypedDict


class TicketState(TypedDict, total=False):
    ticket_id: str
    insurer_id: str
    customer_message: str
    policy_plate: str | None
    # Each document is a plain dict so the checkpointer can store it:
    # {"doc_type", "confidence", "name", "expiry" (ISO date), "plate"}
    documents: list[dict]
    service: str
    status: str
    issues: list[dict]
    outbox: list[str]  # messages queued for the customer
    draft: str
    review_note: str
    reference: str
