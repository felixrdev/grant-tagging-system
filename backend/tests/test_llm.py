import os
from unittest.mock import Mock, patch

from src.llm_refine import llm_refine
from src.tagging import GrantTagger


def test_llm_refine_no_api_key():
    initial_tags = ["agriculture", "education"]

    result = llm_refine("Test Grant", "A grant for farming education", initial_tags)

    assert result == initial_tags


def test_llm_refine_filters_invalid_tags():
    initial_tags = ["agriculture", "education"]

    mock_openai_module = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = (
        "agriculture, education, fake-tag, another-invalid"
    )

    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai_module.OpenAI.return_value = mock_client

    with patch.dict("sys.modules", {"openai": mock_openai_module}):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}):
            result = llm_refine(
                "Test Grant", "A grant for farming education", initial_tags
            )

    assert "agriculture" in result
    assert "education" in result
    assert "fake-tag" not in result
    assert "another-invalid" not in result


def test_llm_refine_handles_exception():
    initial_tags = ["agriculture", "education"]

    mock_openai_module = Mock()
    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mock_openai_module.OpenAI.return_value = mock_client

    with patch.dict("sys.modules", {"openai": mock_openai_module}):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test"}):
            result = llm_refine(
                "Test Grant", "A grant for farming education", initial_tags
            )

    assert result == initial_tags


def test_grant_tagger_use_llm_disabled_by_default():
    tagger = GrantTagger()
    assert tagger.use_llm is False


def test_grant_tagger_use_llm_enabled_via_env():
    with patch.dict(os.environ, {"USE_LLM": "true"}):
        tagger = GrantTagger()
        assert tagger.use_llm is True


def test_grant_tagger_use_llm_enabled_via_param():
    tagger = GrantTagger(use_llm=True)
    assert tagger.use_llm is True


def test_grant_tagger_works_without_llm():
    tagger = GrantTagger(use_llm=False)

    tags = tagger.tag_grant(
        "Farm Education Grant", "Supporting agricultural education programs"
    )

    assert "agriculture" in tags
    assert "education" in tags
    assert isinstance(tags, list)


def test_grant_tagger_llm_enabled_but_no_api_key():
    tagger = GrantTagger(use_llm=True)

    tags = tagger.tag_grant(
        "Farm Education Grant", "Supporting agricultural education programs"
    )

    assert "agriculture" in tags
    assert "education" in tags
    assert isinstance(tags, list)
