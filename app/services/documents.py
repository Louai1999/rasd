"""Validation rules applied to documents after OCR has read them.

OCR and the LLM produce an ExtractedDocument; these rules decide whether the
ticket may continue. Keep this module free of I/O so it stays easy to test.
"""

from dataclasses import dataclass
from datetime import date

from app.domain import REQUIRED_DOCUMENTS, DocumentType, ServiceType

MIN_CONFIDENCE = 0.75


@dataclass(frozen=True)
class ExtractedDocument:
    doc_type: DocumentType
    confidence: float
    name: str | None = None
    expiry: date | None = None
    plate: str | None = None


@dataclass(frozen=True)
class DocumentIssue:
    doc_type: DocumentType
    reason: str  # "missing" | "expired" | "low_confidence" | "plate_mismatch"


def _normalise_plate(plate: str) -> str:
    return "".join(plate.split()).upper()


def check_documents(
    service: ServiceType,
    documents: list[ExtractedDocument],
    *,
    policy_plate: str | None,
    today: date,
) -> list[DocumentIssue]:
    """Return every problem that blocks the ticket. An empty list means complete."""
    by_type = {doc.doc_type: doc for doc in documents}
    issues: list[DocumentIssue] = []

    for required in REQUIRED_DOCUMENTS[service]:
        doc = by_type.get(required)
        if doc is None:
            issues.append(DocumentIssue(required, "missing"))
        elif doc.confidence < MIN_CONFIDENCE:
            issues.append(DocumentIssue(required, "low_confidence"))
        elif doc.expiry is not None and doc.expiry < today:
            issues.append(DocumentIssue(required, "expired"))
        elif (
            required is DocumentType.REGISTRATION
            and policy_plate
            and doc.plate
            and _normalise_plate(doc.plate) != _normalise_plate(policy_plate)
        ):
            issues.append(DocumentIssue(required, "plate_mismatch"))

    return issues
