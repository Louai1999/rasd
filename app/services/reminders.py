"""Per-service polling and reminder rules used by the Temporal workflows."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal

from app.domain import ServiceType


@dataclass(frozen=True)
class ReminderPolicy:
    poll_every: timedelta
    remind_insurer_after: timedelta
    max_insurer_reminders: int
    remind_customer_after: timedelta
    escalate_after: timedelta


# Example defaults. These will move to the settings table so staff can edit them.
DEFAULT_POLICIES: dict[ServiceType, ReminderPolicy] = {
    ServiceType.OWNERSHIP_TRANSFER: ReminderPolicy(
        timedelta(minutes=20), timedelta(hours=24), 3, timedelta(hours=24), timedelta(days=3)
    ),
    ServiceType.UAE_EXTENSION: ReminderPolicy(
        timedelta(minutes=30), timedelta(hours=4), 3, timedelta(hours=6), timedelta(hours=12)
    ),
    ServiceType.POLICY_EXTENSION: ReminderPolicy(
        timedelta(minutes=60), timedelta(hours=24), 2, timedelta(hours=24), timedelta(hours=48)
    ),
    ServiceType.ADD_DRIVER: ReminderPolicy(
        timedelta(minutes=60), timedelta(hours=24), 2, timedelta(hours=24), timedelta(hours=48)
    ),
    ServiceType.CANCELLATION: ReminderPolicy(
        timedelta(hours=2), timedelta(hours=48), 2, timedelta(hours=48), timedelta(days=5)
    ),
}

Action = Literal["wait", "remind", "escalate"]


def next_insurer_action(
    service: ServiceType, *, sent_at: datetime, now: datetime, reminders_sent: int
) -> Action:
    """Decide what to do about an insurer that has not replied yet."""
    policy = DEFAULT_POLICIES[service]
    elapsed = now - sent_at

    if elapsed >= policy.escalate_after:
        return "escalate"
    if elapsed < policy.remind_insurer_after * (reminders_sent + 1):
        return "wait"
    if reminders_sent >= policy.max_insurer_reminders:
        return "escalate"
    return "remind"
