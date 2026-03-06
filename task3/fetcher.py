import asyncio
import random


async def fetch_crm(phone: str):

    await asyncio.sleep(random.uniform(0.2, 0.4))

    return {
        "customer_phone": phone,
        "name": "John Doe",
        "vip": random.choice([True, False]),
        "plan": "Fiber 200Mbps"
    }


async def fetch_billing(phone: str):

    await asyncio.sleep(random.uniform(0.15, 0.35))

    if random.random() < 0.1:
        raise TimeoutError("Billing system timeout")

    return {
        "customer_phone": phone,
        "payment_status": random.choice(["paid", "overdue"]),
        "last_payment_amount": random.randint(40, 120)
    }


async def fetch_ticket_history(phone: str):

    await asyncio.sleep(random.uniform(0.1, 0.3))

    possible_tickets = [
        "slow_internet",
        "router_issue",
        "billing_problem",
        "connection_drop",
        "service_outage"
    ]

    return {
        "customer_phone": phone,
        "tickets": random.sample(possible_tickets, k=3)
    }