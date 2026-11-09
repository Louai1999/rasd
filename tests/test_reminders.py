from datetime import datetime, timedelta

import pytest

from app.domain import ServiceType
from app.services.reminders import next_insurer_action

SENT = datetime(2026, 11, 8, 10, 41)


@pytest.mark.parametrize(
    ("elapsed", "reminders_sent", "expected"),
    [
        (timedelta(minutes=20), 0, "wait"),
        (timedelta(hours=24), 0, "remind"),
        (timedelta(hours=30), 1, "wait"),
        (timedelta(hours=48), 1, "remind"),
        (timedelta(days=3), 2, "escalate"),
    ],
)
def test_transfer_reminder_schedule(elapsed, reminders_sent, expected):
    action = next_insurer_action(
        ServiceType.OWNERSHIP_TRANSFER,
        sent_at=SENT,
        now=SENT + elapsed,
        reminders_sent=reminders_sent,
    )
    assert action == expected


def test_uae_extension_reminds_sooner_than_transfer():
    now = SENT + timedelta(hours=4)
    uae = next_insurer_action(ServiceType.UAE_EXTENSION, sent_at=SENT, now=now, reminders_sent=0)
    transfer = next_insurer_action(
        ServiceType.OWNERSHIP_TRANSFER, sent_at=SENT, now=now, reminders_sent=0
    )
    assert (uae, transfer) == ("remind", "wait")


def test_escalates_after_max_reminders():
    action = next_insurer_action(
        ServiceType.UAE_EXTENSION, sent_at=SENT, now=SENT + timedelta(hours=16), reminders_sent=3
    )
    assert action == "escalate"
