"""Core vocabulary shared by every part of Rasd."""

from enum import StrEnum


class ServiceType(StrEnum):
    OWNERSHIP_TRANSFER = "ownership_transfer"
    UAE_EXTENSION = "uae_extension"
    POLICY_EXTENSION = "policy_extension"
    ADD_DRIVER = "add_driver"
    CANCELLATION = "cancellation"
    UNKNOWN = "unknown"


class TicketStatus(StrEnum):
    NEW = "new"
    AWAITING_DOCUMENTS = "awaiting_documents"
    IN_REVIEW = "in_review"
    SENT_TO_INSURER = "sent_to_insurer"
    AWAITING_INSURER = "awaiting_insurer"
    IN_REVIEW_PAYMENT = "in_review_payment"
    AWAITING_PAYMENT = "awaiting_payment"
    ISSUING = "issuing"
    CLOSED = "closed"
    ESCALATED = "escalated"
    REJECTED = "rejected"


class DocumentType(StrEnum):
    REGISTRATION = "registration"
    ID_CARD = "id_card"
    DRIVING_LICENCE = "driving_licence"


# Documents the customer must provide for each service.
# Insurer-specific extras come from the RAG knowledge base later.
REQUIRED_DOCUMENTS: dict[ServiceType, list[DocumentType]] = {
    ServiceType.OWNERSHIP_TRANSFER: [
        DocumentType.REGISTRATION,
        DocumentType.ID_CARD,
        DocumentType.DRIVING_LICENCE,
    ],
    ServiceType.UAE_EXTENSION: [],
    ServiceType.POLICY_EXTENSION: [DocumentType.REGISTRATION, DocumentType.DRIVING_LICENCE],
    ServiceType.ADD_DRIVER: [DocumentType.ID_CARD, DocumentType.DRIVING_LICENCE],
    ServiceType.CANCELLATION: [],
    ServiceType.UNKNOWN: [],
}
