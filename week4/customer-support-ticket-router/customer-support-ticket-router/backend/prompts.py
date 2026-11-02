"""Prompt templates. Each technique is a separate function."""
import json

SYSTEM_RULES = """
You classify customer support emails. Return only one JSON object matching this schema:
{
  "category": "billing | technical | delivery | account | other",
  "priority": "low | medium | high",
  "product": "product/service named in the email, or Unknown",
  "customer_wants": "refund | fix | information | cancel"
}
Use only the allowed values. Do not invent product names.
Priority guide: high = access blocked, serious outage, urgent/major impact;
medium = a concrete problem needing support but not clearly urgent;
low = general information or non-urgent request.
Category guide: billing=charges/payments/invoices; technical=bugs/errors/performance;
delivery=shipping/tracking/missing parcel; account=login/profile/account access;
other=anything else.
Customer wants: refund=money back/charge reversal; fix=repair or resolve a problem;
information=an answer or explanation; cancel=stop a plan/order/service.
If more than one intent exists, choose the main request.
"""

def zero_shot_prompt(email: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_RULES},
        {"role": "user", "content": f"Classify this email. Return JSON only.\nEMAIL:\n{email}"},
    ]

def few_shot_prompt(email: str) -> list[dict]:
    examples = [
        {
            "input": "I was charged twice for my Premium plan. Please return the extra payment.",
            "output": {"category": "billing", "priority": "medium", "product": "Premium plan", "customer_wants": "refund"},
        },
        {
            "input": "The app closes every time I press Sign In. Please fix it.",
            "output": {"category": "technical", "priority": "high", "product": "app", "customer_wants": "fix"},
        },
        {
            "input": "Where is my parcel? The tracking page has not updated.",
            "output": {"category": "delivery", "priority": "medium", "product": "parcel", "customer_wants": "information"},
        },
    ]
    examples_text = json.dumps(examples, ensure_ascii=False, indent=2)
    return [
        {"role": "system", "content": SYSTEM_RULES},
        {"role": "user", "content": f"Here are labelled examples:\n{examples_text}\n\nNow classify this new email. Do not copy an example's answer unless it fits. Return JSON only.\nEMAIL:\n{email}"},
    ]

def role_based_prompt(email: str) -> list[dict]:
    role = (
        "You are a careful senior customer-support triage specialist. "
        "Your job is to label tickets consistently for a support queue. "
        "Use the policy definitions, avoid assumptions, and return only valid JSON."
    )
    return [
        {"role": "system", "content": role + "\n" + SYSTEM_RULES},
        {"role": "user", "content": f"Classify this support email using the required schema.\nEMAIL:\n{email}"},
    ]
def chain_of_thought_prompt(ticket: str) -> str:
    return f"""
You are a customer support ticket classification assistant.

Analyse the ticket using these steps:
1. Identify the customer's main issue.
2. Determine the appropriate category.
3. Assess urgency to select a priority.
4. Identify the product mentioned.
5. Determine what the customer wants.

Use these allowed values:
- category: billing, technical, delivery, account, other
- priority: low, medium, high
- customer_wants: refund, fix, information, cancel

Return only valid JSON matching this structure:
{{
    "category": "...",
    "priority": "...",
    "product": "...",
    "customer_wants": "..."
}}

Ticket:
{ticket}
"""
PROMPT_FUNCTIONS = {
    "zero_shot": zero_shot_prompt,
    "few_shot": few_shot_prompt,
    "role_based": role_based_prompt,
    "chain_of_thought": chain_of_thought_prompt,

}
def select_prompt_technique(email: str) -> str:
    """Choose a prompt technique based on the support email."""

    text = email.lower()

    billing_keywords = [
        "refund", "payment", "charged", "billing", "invoice"
    ]

    technical_keywords = [
        "error", "crash", "not working", "bug", "technical"
    ]

    delivery_keywords = [
        "delivery", "parcel", "tracking", "shipment", "package"
    ]

    if any(word in text for word in billing_keywords):
        return "few_shot"

    if any(word in text for word in technical_keywords):
        return "role_based"

    if any(word in text for word in delivery_keywords):
        return "zero_shot"

    return "few_shot"