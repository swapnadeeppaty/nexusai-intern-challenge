# NexusAI Internship Challenge — Written Answers

---

# Q1 — Should we query the database on partial transcripts?

Speech-to-text systems often produce partial transcripts every few hundred milliseconds while the customer is still speaking. Querying the database immediately on each partial transcript could reduce latency because the system can begin fetching relevant customer data before the user finishes speaking. However, this approach introduces the risk of acting on incomplete or incorrect intent detection.

A practical solution is a hybrid approach. The system can begin lightweight background tasks such as fetching customer account information or recent ticket history once a partial transcript suggests a probable intent. However, critical decisions such as escalation or AI response generation should wait until the final transcript is confirmed. This reduces response latency without introducing incorrect decisions.

Another improvement would be maintaining a confidence threshold for partial transcripts. If intent detection confidence exceeds a certain threshold, early database queries can be triggered safely. Otherwise, the system waits for the final transcript. This approach balances performance improvements with decision accuracy.

---

# Q2 — Risks of auto-adding high CSAT resolutions to the knowledge base

Automatically adding solutions with CSAT ≥ 4 to a knowledge base may appear beneficial, but it can introduce several long-term problems.

One potential issue is the gradual accumulation of incorrect or overly specific solutions. A high CSAT score may reflect customer satisfaction with the agent rather than the correctness of the solution itself. Over several months, this could pollute the knowledge base with inaccurate troubleshooting steps that reduce AI reliability.

Another risk is context-specific solutions being generalized incorrectly. For example, a fix that works for a specific router model or regional network issue may be automatically applied to unrelated cases, leading to incorrect recommendations.

To prevent these problems, automated knowledge additions should pass through a validation layer. One method is clustering similar solutions and only promoting solutions that consistently produce high CSAT across multiple customers. Another safeguard is periodic human review of newly added knowledge entries. Combining automated filtering with human oversight ensures the knowledge base improves over time rather than degrading.

---

# Q3 — Handling an angry customer requesting cancellation

In this scenario, the customer expresses frustration, repeated service failure, and an immediate request for cancellation. The system first receives the transcript and runs sentiment analysis. The phrase “your company is useless and I want to cancel right now” would likely produce a strongly negative sentiment score.

The escalation engine then evaluates the decision rules. The intent would be classified as `service_cancellation`, which automatically triggers escalation regardless of other signals. Additionally, the negative sentiment would also trigger the angry customer rule.

Before escalation, the AI should acknowledge the customer’s frustration in a short response such as:
“I’m sorry you’ve experienced these issues. I’m transferring you to a specialist who can assist with your request right away.”

At the same time, the system forwards context to the human agent, including the transcript, detected intent, customer history, billing status, and previous complaints. Providing this context ensures the human agent can resolve the situation quickly without asking the customer to repeat information.

---

# Q4 — One improvement to the system

One of the most valuable improvements to this system would be an automated outage detection layer. Many customer complaints arise from regional outages rather than individual technical issues. If the AI assistant attempts to troubleshoot every complaint individually, it wastes time and frustrates customers.

An outage detection module could monitor incoming tickets and identify unusual spikes in similar complaints from the same geographic region. If many users report “no internet” within a short period, the system can infer a likely service outage.

Once detected, the AI assistant could immediately inform customers about the outage and estimated repair time instead of asking them to restart routers or run diagnostics. This significantly reduces unnecessary troubleshooting interactions and improves customer satisfaction.

The effectiveness of this feature could be measured by reduced average call duration, improved CSAT scores during outage events, and fewer escalations to human agents.
