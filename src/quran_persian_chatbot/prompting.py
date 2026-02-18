from __future__ import annotations

SYSTEM_INSTRUCTION = (
    "تو یک دستیار فارسی زبان هستی که فقط بر اساس منابع داده‌شده درباره قرآن پاسخ می‌دهد. "
    "اگر سوال نامرتبط بود یا پاسخ در اطلاعات موجود نبود، واضح بگو اطلاعات کافی نداری. "
    "مرحله فکر کردن داخلی را نمایش نده."
)


def build_rag_prompt(query: str, context: str) -> str:
    safe_context = context.strip() if context.strip() else "اطلاعات مرتبطی پیدا نشد."
    return (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"اطلاعات:\n{safe_context}\n\n"
        f"سوال کاربر:\n{query.strip()}\n"
    )
