# Intern Challenge

This repository contains my implementation of the **NexusAI Backend Internship Challenge**.
The project simulates an AI-powered telecom customer support backend that processes messages, fetches customer data from multiple systems, and decides whether to escalate cases to human agents.

---

# Project Structure

```
nexusai-intern-challenge
│
├── task1/   # AI message handler using OpenAI
├── task2/   # PostgreSQL schema and repository layer
├── task3/   # Async parallel data fetching simulation
├── task4/   # Escalation decision engine with pytest tests
│
├── README.md
├── requirements.txt
└── ANSWERS.md
```

---

# Setup Instructions

Clone the repository:

```
git clone https://github.com/swapnadeeppaty/nexusai-intern-challenge.git
cd nexusai-intern-challenge
```

Install dependencies:

```
pip install -r requirements.txt
```

Set OpenAI API key (required for Task 1):

Mac/Linux:

```
export OPENAI_API_KEY="your_api_key"
```

Windows:

```
set OPENAI_API_KEY=your_api_key
```

---

# Task 1 — AI Message Handler

File:

```
task1/handler.py
```

Implements an async function:

```
handle_message(customer_message, customer_id, channel)
```

Features:

* Uses OpenAI API
* Telecom support system prompt
* Structured response using `MessageResponse` dataclass
* Handles error cases:

  * Empty input
  * API timeout (10 seconds)
  * Rate limit retry after 2 seconds
* Channel-specific formatting for voice, chat, and WhatsApp

---

# Task 2 — Database Schema

Files:

```
task2/schema.sql
task2/repository.py
```

Features:

* PostgreSQL table for storing customer interactions
* Data constraints:

  * confidence_score between 0–1
  * CSAT score between 1–5
* Performance indexes:

  * customer_phone lookup
  * intent analytics
  * recent call retrieval

Repository class methods:

```
save(call_data)
get_recent(phone, limit)
get_low_resolution_intents()
```

---

# Task 3 — Parallel Data Fetcher

File:

```
task3/fetcher.py
```

Simulates three external systems:

* CRM service
* Billing service
* Ticket history service

Two implementations:

Sequential fetch:

```
CRM → Billing → Tickets
```

Parallel fetch:

```
asyncio.gather(CRM, Billing, Tickets)
```

Example timing results:

Sequential fetch took ~700 ms
Parallel fetch took ~300 ms

Parallel execution is roughly **2x faster**, demonstrating the benefit of asynchronous concurrency.

---

# Task 4 — Escalation Decision Engine

Files:

```
task4/escalation.py
task4/test_escalation.py
```

Function:

```
should_escalate(context, confidence_score, sentiment_score, intent)
```

Rules implemented:

1. Low confidence (<0.65)
2. Angry customer sentiment (< -0.6)
3. Repeat complaint (same intent ≥3 times)
4. Service cancellation
5. VIP customer with overdue billing
6. Incomplete data with confidence <0.80

Tests:

```
pytest task4/ -v
```

All tests pass successfully.

---

# Rule Conflict Handling

If multiple escalation rules apply simultaneously, the system returns the first matching rule based on priority order. Critical rules such as **service cancellation and angry customers** are checked earlier because they represent higher-risk interactions requiring human intervention.

For example, if confidence is high but the intent is `service_cancellation`, escalation still occurs because cancellation requests involve account-level decisions that should be handled by human agents.

---

# Technologies Used

* Python 3.11
* Asyncio
* OpenAI API
* PostgreSQL
* asyncpg
* pytest
