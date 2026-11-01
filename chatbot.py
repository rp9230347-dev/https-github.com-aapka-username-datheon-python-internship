"""Task 3 - Rule-based customer support chatbot (keywords + regex)."""
import json
import os
import re
from datetime import datetime

BUSINESS_NAME = "TechMart"
HOURS = {
    "weekdays": "9:00 AM - 8:00 PM (Mon-Fri)",
    "weekend": "10:00 AM - 6:00 PM (Sat-Sun)",
}

# intent -> (regex pattern, response)
INTENTS = {
    "greeting": (r"\b(hi|hello|hey|good (morning|afternoon|evening))\b",
                 f"Hello! Welcome to {BUSINESS_NAME}. How can I help you today?"),
    "hours": (r"\b(hours?|open|opening|close|closing|timings?|time)\b",
              f"We're open {HOURS['weekdays']} and {HOURS['weekend']}."),
    "price": (r"\b(price|cost|how much|pricing)\b",
              "Prices vary by product. Laptops start at Rs. 35,000, phones at Rs. 8,000 and accessories at Rs. 299."),
    "shipping": (r"\b(ship(ping)?|deliver(y)?|dispatch)\b",
                 "Standard delivery takes 3-5 business days. Free shipping on orders above Rs. 999."),
    "return": (r"\b(return|refund|exchange|replace(ment)?)\b",
               "You can return any product within 7 days of delivery. Refunds take 5-7 working days."),
    "warranty": (r"\b(warranty|guarantee)\b",
                 "All electronics include a 1-year manufacturer warranty."),
    "payment": (r"\b(pay(ment)?|upi|card|cod|cash on delivery)\b",
                "We accept UPI, credit/debit cards, net banking and Cash on Delivery."),
    "order_status": (r"\b(track|order status|where is my order|order)\b",
                     "To track your order, share your order ID (e.g. ORD12345) and I'll check it."),
    "contact": (r"\b(contact|phone|email|support|call|reach)\b",
                "Reach us at support@techmart.example or call 1800-123-456 (toll free)."),
    "thanks": (r"\b(thanks|thank you|thx)\b", "You're welcome! Anything else I can help with?"),
}

ORDER_ID = re.compile(r"\bORD\d{4,}\b", re.IGNORECASE)
EXIT_WORDS = {"bye", "exit", "quit"}
FALLBACK = ("Sorry, I didn't understand that. You can ask about business hours, prices, "
            "shipping, returns, warranty, payment or order tracking.")


def load_faqs(path=None):
    """Load extra FAQ entries from sample_faq.json (optional)."""
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_faq.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f).get("faqs", [])
    except (OSError, ValueError):
        return []


FAQS = load_faqs()
STOP = {"the", "a", "an", "do", "i", "my", "your", "are", "is", "will", "when", "how", "what", "to", "of", "you"}


def faq_answer(text: str):
    """Return the FAQ answer sharing the most keywords with the user text (needs 2+)."""
    words = set(re.findall(r"[a-z]+", text)) - STOP
    best, score = None, 1
    for item in FAQS:
        overlap = len(words & (set(re.findall(r"[a-z]+", item["question"].lower())) - STOP))
        if overlap > score:
            best, score = item["answer"], overlap
    return best


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def get_response(text: str, state: dict) -> str:
    # Order IDs get a contextual reply
    m = ORDER_ID.search(text)
    if m:
        state["last_intent"] = "order_status"
        return f"Order {m.group().upper()} is being processed and will be dispatched within 24 hours."

    # "is it open now?" style contextual answer
    if re.search(r"\bopen (now|today)\b", text):
        now = datetime.now()
        open_now = (9 <= now.hour < 20) if now.weekday() < 5 else (10 <= now.hour < 18)
        state["last_intent"] = "hours"
        return "Yes, we're open right now!" if open_now else f"We're closed right now. Hours: {HOURS['weekdays']}; {HOURS['weekend']}."

    # Match keywords/regex intents
    for intent, (pattern, reply) in INTENTS.items():
        if re.search(pattern, text):
            state["last_intent"] = intent
            return reply

    faq = faq_answer(text)
    if faq:
        return faq

    state["fallbacks"] += 1
    if state["fallbacks"] >= 3:
        return FALLBACK + " You can also email support@techmart.example for human help."
    return FALLBACK


def main():
    state = {"last_intent": None, "fallbacks": 0}  # conversation state
    print(f"{BUSINESS_NAME} Assistant (type 'bye', 'exit' or 'quit' to leave)")
    print("-" * 55)
    while True:
        try:
            raw = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break
        text = normalize(raw)
        if not text:
            continue
        if text in EXIT_WORDS:
            print("Bot: Thanks for visiting! Goodbye.")
            break
        print("Bot:", get_response(text, state))


if __name__ == "__main__":
    main()
