from src.synonyms import resolve_query, resolve_synonym


def test_resolve_synonym_basic():
    assert resolve_synonym("learning") == "education"
    assert resolve_synonym("teach") == "education"
    assert resolve_synonym("school") == "education"


def test_resolve_synonym_multiword():
    assert resolve_synonym("local food") == "local-food"
    assert resolve_synonym("soil health") == "soil"
    assert resolve_synonym("water system") == "water"


def test_resolve_synonym_passthrough():
    assert resolve_synonym("agriculture") == "agriculture"
    assert resolve_synonym("unknown-term") == "unknown-term"


def test_resolve_query_single_word():
    tags = resolve_query("learning")
    assert "education" in tags


def test_resolve_query_multiple_words():
    tags = resolve_query("learning soil")
    assert "education" in tags
    assert "soil" in tags


def test_resolve_query_multiword_phrase():
    tags = resolve_query("local food")
    assert "local-food" in tags


def test_resolve_query_hyphenated():
    tags = resolve_query("soil-health")
    assert "soil" in tags


def test_resolve_query_mixed():
    tags = resolve_query("irrigation farming student")
    assert "water" in tags
    assert "agriculture" in tags
    assert "youth" in tags
