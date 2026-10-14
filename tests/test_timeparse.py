import pytest

from datetime import datetime
from timeparse import parse_time

BASE = datetime(2026, 10, 10, 9, 15, 30, 123456)


@pytest.mark.parametrize(
    ("text", "hour", "minute"),
    [
        ("3pm", 15, 0),
        ("3 pm", 15, 0),
        ("3:30 PM", 15, 30),
        ("3:00pm", 15, 0),
        ("15:00", 15, 0),
        ("12:00 am", 0, 0),
        ("3:00 p.m.", 15, 0),
        ("noon", 12, 0),
        ("midday", 12, 0),
        ("midnight", 0, 0),
        ("  Noon  ", 12, 0),
        ("MIDDAY", 12, 0),
        ("  MIDNIGHT    ", 0, 0),
        ("06:54 P.M.", 18, 54)
    ],
)
def test_parse_time_understands_expected_formats(text, hour, minute):
    result = parse_time(text, base=BASE)

    assert (result.hour, result.minute) == (hour, minute)


def test_parse_time_anchors_to_base_date_and_zeroes_seconds():
    result = parse_time("3pm", base=BASE)

    assert result.date() == BASE.date()
    assert result.second == 0
    assert result.microsecond == 0


def test_parse_time_defaults_base_to_now():
    before = datetime.now()
    result = parse_time("3pm")
    after = datetime.now()

    assert before.date() <= result.date() <= after.date()


@pytest.mark.parametrize("text", ["banana", "3", "3 o'clock", "tomorrow", ""])
def test_parse_time_raises_instead_of_guessing(text):
    with pytest.raises(ValueError):
        parse_time(text, base=BASE)
