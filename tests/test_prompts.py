import pytest

from prompts import (
    INTENT_CLASSIFICATION_PROMPT,
    PRODUCTIVITY_PROMPT,
    LOCATION_QUERY_PROMPT,
    GENERAL_QUERY,
    classify_intent_prompt,
    handle_productivity,
    handle_location_query,
    handle_general_query,
)


def test_classify_intent_prompt_includes_user_input():
    user_input = "Add a task to buy groceries"

    result = classify_intent_prompt(user_input)

    assert user_input in result
    assert "TASK_MANAGEMENT" in result
    assert "TASK_QUERY" in result
    assert "PRODUCTIVITY" in result
    assert "LOCATION_QUERY" in result
    assert "GENERAL_QUERY" in result
    assert "UNKNOWN" in result
    assert "brief explanation" in result


def test_classify_intent_prompt_empty_input():
    result = classify_intent_prompt("")

    assert "User input:" in result
    assert INTENT_CLASSIFICATION_PROMPT.format(user_input="") == result


def test_handle_productivity_includes_query():
    query = "Help me focus on my work"

    result = handle_productivity({"query": query})

    assert query in result
    assert "2-3 practical, actionable tips" in result
    assert "ACTION:" in result
    assert "TIME:" in result
    assert "DURATION:" in result


def test_handle_productivity_missing_query():
    result = handle_productivity({})

    assert "User query:" in result
    assert PRODUCTIVITY_PROMPT.format(query="") == result


def test_handle_location_query_includes_query():
    query = "Find coffee shops in San Francisco"

    result = handle_location_query({"query": query})

    assert query in result
    assert "2-3 places or options" in result
    assert "specific location" in result


def test_handle_location_query_missing_query():
    result = handle_location_query({})

    assert LOCATION_QUERY_PROMPT.format(query="") == result


def test_handle_general_query_includes_query():
    query = "What tasks do I have this week?"

    result = handle_general_query({"query": query})

    assert query in result
    assert "helpful and informative response" in result


def test_handle_general_query_missing_query():
    result = handle_general_query({})

    assert GENERAL_QUERY.format(query="") == result


@pytest.mark.parametrize(
    "query",
    [
        "Buy groceries",
        "What's my schedule?",
        "Plan my workday",
        "",
        "Text with {braces} and special characters!",
    ],
)
def test_prompt_functions_preserve_query_text(query):
    assert query in classify_intent_prompt(query)
    assert query in handle_productivity({"query": query})
    assert query in handle_location_query({"query": query})
    assert query in handle_general_query({"query": query})


def test_prompt_functions_handle_missing_query_key():
    data = {}

    assert handle_productivity(data) == PRODUCTIVITY_PROMPT.format(query="")
    assert handle_location_query(data) == LOCATION_QUERY_PROMPT.format(query="")
    assert handle_general_query(data) == GENERAL_QUERY.format(query="")
