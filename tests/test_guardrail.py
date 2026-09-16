from src.guardrail import evaluate, scan


def decision(tool, text, data_class="public"):
    return evaluate(tool, text, data_class, write_audit=False)["decision"]


def test_detects_password():
    assert "password" in scan("password: DontShareMe123")


def test_detects_email():
    assert "email" in scan("Contact person@example.com before sending")


def test_detects_api_key_label():
    assert "api_key" in scan("api_key=abcdefgh12345678")


def test_safe_public_prompt_allowed():
    assert decision("company-chat-ai", "Summarize this public announcement") == "ALLOW"


def test_internal_prompt_allowed_for_company_tool():
    assert decision("company-chat-ai", "Summarize the internal operating guide", "internal") == "ALLOW"


def test_customer_prompt_requires_review():
    assert decision("company-chat-ai", "Summarize the approved customer briefing", "customer") == "REVIEW"


def test_confidential_prompt_requires_review():
    assert decision("company-chat-ai", "Review the architecture overview", "confidential") == "REVIEW"


def test_unapproved_tool_blocked():
    assert decision("unapproved-ai", "hello") == "BLOCK"


def test_public_demo_blocks_internal_data():
    assert decision("public-ai-demo", "internal planning notes", "internal") == "BLOCK"


def test_sensitive_content_blocks_even_on_approved_tool():
    assert decision("company-chat-ai", "password: DontShareMe123", "internal") == "BLOCK"
