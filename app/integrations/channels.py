"""The contract between the agent (LangGraph) and the ways we reach insurers.

The agent only talks to an InsurerChannel. Email and the Playwright portal
client each implement it, so both halves of the team can work in parallel.
"""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class InsurerRequest:
    ticket_id: str
    insurer_id: str
    service: str
    body: str
    attachments: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SubmissionReceipt:
    reference: str
    channel: str  # "email" | "portal"


class InsurerChannel(Protocol):
    def submit(self, request: InsurerRequest) -> SubmissionReceipt: ...


class FakeChannel:
    """In-memory channel for tests and local demos."""

    def __init__(self) -> None:
        self.sent: list[InsurerRequest] = []

    def submit(self, request: InsurerRequest) -> SubmissionReceipt:
        self.sent.append(request)
        return SubmissionReceipt(reference=f"FAKE-{len(self.sent)}", channel="fake")
