from fastapi import FastAPI

from app.domain import REQUIRED_DOCUMENTS, ServiceType

app = FastAPI(title="Rasd", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/services")
def services() -> dict[str, list[str]]:
    """Required documents per service, used by the staff screens."""
    return {
        service.value: [doc.value for doc in docs]
        for service, docs in REQUIRED_DOCUMENTS.items()
        if service is not ServiceType.UNKNOWN
    }
