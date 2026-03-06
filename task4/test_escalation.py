import pytest
from task4.escalation import should_escalate
from task3.fetcher import CustomerContext


def create_context(
    vip=False,
    payment_status="paid",
    tickets=None,
    data_complete=True
):
    return CustomerContext(
        crm={"vip": vip},
        billing={"payment_status": payment_status},
        tickets={"tickets": tickets or []},
        data_complete=data_complete,
        fetch_time_ms=200
    )


def test_low_confidence():
    """AI must escalate if confidence score is below 0.65."""
    context = create_context()
    result = should_escalate(context, 0.5, 0.0, "router_issue")
    assert result == (True, "low_confidence")


def test_angry_customer():
    """Highly negative sentiment should trigger escalation."""
    context = create_context()
    result = should_escalate(context, 0.9, -0.8, "router_issue")
    assert result == (True, "angry_customer")


def test_repeat_complaint():
    """Escalate when the same complaint appears at least three times."""
    context = create_context(tickets=["slow_internet", "slow_internet", "slow_internet"])
    result = should_escalate(context, 0.9, 0.0, "slow_internet")
    assert result == (True, "repeat_complaint")


def test_service_cancellation():
    """Service cancellation requests must always escalate."""
    context = create_context()
    result = should_escalate(context, 0.95, 0.0, "service_cancellation")
    assert result == (True, "service_cancellation")


def test_vip_overdue():
    """VIP customers with overdue billing should escalate to human agents."""
    context = create_context(vip=True, payment_status="overdue")
    result = should_escalate(context, 0.9, 0.0, "billing_problem")
    assert result == (True, "vip_overdue")


def test_incomplete_data():
    """If system data is incomplete and confidence is below 0.80, escalate."""
    context = create_context(data_complete=False)
    result = should_escalate(context, 0.7, 0.0, "router_issue")
    assert result == (True, "incomplete_data")


def test_handled_by_ai():
    """If none of the escalation rules trigger, AI should handle the case."""
    context = create_context()
    result = should_escalate(context, 0.9, 0.0, "router_issue")
    assert result == (False, "handled_by_ai")


def test_edge_confidence_boundary():
    """Confidence exactly at 0.65 should NOT trigger low confidence escalation."""
    context = create_context()
    result = should_escalate(context, 0.65, 0.0, "router_issue")
    assert result == (False, "handled_by_ai")