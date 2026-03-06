from task3.fetcher import CustomerContext


def should_escalate(
    context: CustomerContext,
    confidence_score: float,
    sentiment_score: float,
    intent: str
) -> tuple:
    """
    Decide whether the AI should escalate the interaction to a human agent.

    Returns:
        (bool, str): (should_escalate, reason)
    """

    # Rule 1: Low confidence
    if confidence_score < 0.65:
        return True, "low_confidence"

    # Rule 2: Angry customer sentiment
    if sentiment_score < -0.6:
        return True, "angry_customer"

    # Rule 3: Repeat complaint
    if context.tickets:
        ticket_list = context.tickets.get("tickets", [])
        if ticket_list.count(intent) >= 3:
            return True, "repeat_complaint"

    # Rule 4: Service cancellation always escalates
    if intent == "service_cancellation":
        return True, "service_cancellation"

    # Rule 5: VIP customer with overdue billing
    if context.crm and context.billing:
        if context.crm.get("vip") and context.billing.get("payment_status") == "overdue":
            return True, "vip_overdue"

    # Rule 6: Incomplete data with moderate confidence
    if not context.data_complete and confidence_score < 0.80:
        return True, "incomplete_data"

    # Default case
    return False, "handled_by_ai"