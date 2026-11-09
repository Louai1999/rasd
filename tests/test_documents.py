from datetime import date

from app.domain import DocumentType, ServiceType
from app.services.documents import ExtractedDocument, check_documents

TODAY = date(2026, 11, 9)


def doc(doc_type, *, confidence=0.95, expiry=date(2029, 1, 1), plate=None):
    return ExtractedDocument(doc_type=doc_type, confidence=confidence, expiry=expiry, plate=plate)


def reasons(issues):
    return {(i.doc_type, i.reason) for i in issues}


def test_transfer_with_all_documents_is_complete():
    docs = [
        doc(DocumentType.REGISTRATION, plate="12345 RB"),
        doc(DocumentType.ID_CARD),
        doc(DocumentType.DRIVING_LICENCE),
    ]
    issues = check_documents(
        ServiceType.OWNERSHIP_TRANSFER, docs, policy_plate="12345rb", today=TODAY
    )
    assert issues == []


def test_missing_licence_blocks_transfer():
    docs = [doc(DocumentType.REGISTRATION), doc(DocumentType.ID_CARD)]
    issues = check_documents(ServiceType.OWNERSHIP_TRANSFER, docs, policy_plate=None, today=TODAY)
    assert reasons(issues) == {(DocumentType.DRIVING_LICENCE, "missing")}


def test_expired_licence_is_flagged():
    docs = [
        doc(DocumentType.REGISTRATION),
        doc(DocumentType.DRIVING_LICENCE, expiry=date(2026, 8, 14)),
    ]
    issues = check_documents(ServiceType.POLICY_EXTENSION, docs, policy_plate=None, today=TODAY)
    assert reasons(issues) == {(DocumentType.DRIVING_LICENCE, "expired")}


def test_blurry_scan_is_flagged_as_low_confidence():
    docs = [doc(DocumentType.REGISTRATION, confidence=0.58), doc(DocumentType.DRIVING_LICENCE)]
    issues = check_documents(ServiceType.POLICY_EXTENSION, docs, policy_plate=None, today=TODAY)
    assert reasons(issues) == {(DocumentType.REGISTRATION, "low_confidence")}


def test_plate_mismatch_is_flagged():
    docs = [doc(DocumentType.REGISTRATION, plate="999 AA"), doc(DocumentType.DRIVING_LICENCE)]
    issues = check_documents(
        ServiceType.POLICY_EXTENSION, docs, policy_plate="12345 RB", today=TODAY
    )
    assert reasons(issues) == {(DocumentType.REGISTRATION, "plate_mismatch")}


def test_uae_extension_needs_no_customer_documents():
    assert check_documents(ServiceType.UAE_EXTENSION, [], policy_plate=None, today=TODAY) == []
