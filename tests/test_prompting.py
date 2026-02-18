from quran_persian_chatbot.prompting import build_rag_prompt


def test_build_rag_prompt_contains_query_and_context() -> None:
    prompt = build_rag_prompt(query="تفسیر سوره حمد چیست؟", context="متن نمونه")

    assert "تفسیر سوره حمد چیست؟" in prompt
    assert "متن نمونه" in prompt


def test_build_rag_prompt_handles_empty_context() -> None:
    prompt = build_rag_prompt(query="سوال", context="   ")

    assert "اطلاعات مرتبطی پیدا نشد." in prompt
