import subprocess
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

import tw


@patch("tw.tw.get_tasks")
def test_get_tasks_filters_by_date(mock_get_tasks):
    expected = [Mock(description="Finish report")]
    mock_get_tasks.return_value = expected

    result = tw.get_tasks(
        datetime(2026, 10, 1),
        datetime(2026, 11, 1),
    )

    assert result == expected
    mock_get_tasks.assert_called_once_with(
        "due.after:2026-10-01 due.before:2026-11-01"
    )


@patch("tw.tw.add_task")
def test_add_task_passes_summary_and_due_date(mock_add_task):
    task = {
        "summary": "Finish report",
        "due": datetime(2026, 10, 15, 17, 30),
    }

    tw.add_task(task)

    dto = mock_add_task.call_args.args[0]
    assert dto.description == "Finish report"
    assert dto.due == "2026-10-15T17:30:00"


@patch("tw.tw.done_task")
def test_complete_task_returns_true(mock_done_task):
    assert tw.complete_task("task-uuid") is True
    mock_done_task.assert_called_once_with("task-uuid")


@patch("tw.tw.done_task", side_effect=Exception("Task not found"))
def test_complete_task_returns_false_on_error(mock_done_task):
    assert tw.complete_task("invalid-uuid") is False


@patch("tw.tw.get_tasks")
def test_get_completed_tasks_filters_by_status(mock_get_tasks):
    expected = [Mock(description="Completed report")]
    mock_get_tasks.return_value = expected

    result = tw.get_completed_tasks()

    assert result == expected
    mock_get_tasks.assert_called_once_with("status:completed")
