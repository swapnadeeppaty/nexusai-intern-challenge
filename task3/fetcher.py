import asyncio
import random
import time
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class CustomerContext:
    crm: Optional[Dict]
    billing: Optional[Dict]
    tickets: Optional[Dict]
    data_complete: bool
    fetch_time_ms: float


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

    # 10% chance of timeout
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


async def fetch_sequential(phone: str):

    start_time = time.perf_counter()

    crm_data = await fetch_crm(phone)
    billing_data = await fetch_billing(phone)
    ticket_data = await fetch_ticket_history(phone)

    end_time = time.perf_counter()

    elapsed = (end_time - start_time) * 1000

    print(f"Sequential fetch took {elapsed:.2f} ms")

    data_complete = all([
        crm_data is not None,
        billing_data is not None,
        ticket_data is not None
    ])

    return CustomerContext(
        crm=crm_data,
        billing=billing_data,
        tickets=ticket_data,
        data_complete=data_complete,
        fetch_time_ms=elapsed
    )


async def fetch_parallel(phone: str):

    start_time = time.perf_counter()

    results = await asyncio.gather(
        fetch_crm(phone),
        fetch_billing(phone),
        fetch_ticket_history(phone),
        return_exceptions=True
    )

    crm_data, billing_data, ticket_data = results

    if isinstance(billing_data, Exception):
        print("Warning: billing fetch failed")
        billing_data = None

    end_time = time.perf_counter()

    elapsed = (end_time - start_time) * 1000

    print(f"Parallel fetch took {elapsed:.2f} ms")

    data_complete = all([
        crm_data is not None,
        billing_data is not None,
        ticket_data is not None
    ])

    return CustomerContext(
        crm=crm_data,
        billing=billing_data,
        tickets=ticket_data,
        data_complete=data_complete,
        fetch_time_ms=elapsed
    )