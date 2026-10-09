import asyncio
from unittest.mock import AsyncMock, patch

import llm
from config import BASE_MODEL


class FakeClient:
    def __init__(self, *, chat=None, list_=None):
        self.chat = chat
        self.list = list_

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False


def _reply(text: str) -> dict:
    return {"message": {"content": text}}


@patch("llm._client")
def test_run_prompt_returns_trimmed_reply(mock_client):
    chat = AsyncMock(return_value=_reply("  hello  "))
    mock_client.return_value = FakeClient(chat=chat)

    result = asyncio.run(llm.run_prompt("hi"))

    assert result == "hello"
    chat.assert_awaited_once_with(
        model=BASE_MODEL,
        messages=[{"role": "user", "content": "hi"}],
        stream=False,
    )


@patch("llm._client")
def test_run_prompt_accepts_model_override(mock_client):
    chat = AsyncMock(return_value=_reply("ok"))
    mock_client.return_value = FakeClient(chat=chat)

    asyncio.run(llm.run_prompt("hi", model="other:1b"))

    assert chat.call_args.kwargs["model"] == "other:1b"


@patch("llm._client")
def test_run_prompts_returns_replies_in_order(mock_client):
    chat = AsyncMock(
        side_effect=lambda model, messages, stream: _reply(
            messages[0]["content"].upper()
        )
    )
    mock_client.return_value = FakeClient(chat=chat)

    results = asyncio.run(llm.run_prompts(["one", "two", "three"]))

    assert results == ["ONE", "TWO", "THREE"]
    assert chat.await_count == 3


@patch("llm._client")
def test_run_prompts_empty_does_not_open_a_client(mock_client):
    assert asyncio.run(llm.run_prompts([])) == []
    mock_client.assert_not_called()


@patch("llm._client")
def test_run_prompts_runs_concurrently(mock_client):
    state = {"active": 0, "peak": 0}

    async def chat(model, messages, stream):
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        await asyncio.sleep(0.02)
        state["active"] -= 1
        return _reply(messages[0]["content"])

    mock_client.return_value = FakeClient(chat=chat)

    asyncio.run(llm.run_prompts(["a", "b", "c"]))

    # Sequential execution would never see more than one active call.
    assert state["peak"] == 3


@patch("llm._client")
def test_check_host_true_when_reachable(mock_client):
    mock_client.return_value = FakeClient(list_=AsyncMock(return_value={"models": []}))

    assert asyncio.run(llm.check_host()) is True


@patch("llm._client")
def test_check_host_false_when_unreachable(mock_client):
    list_call = AsyncMock(side_effect=ConnectionError("no route to host"))
    mock_client.return_value = FakeClient(list_=list_call)

    assert asyncio.run(llm.check_host()) is False
