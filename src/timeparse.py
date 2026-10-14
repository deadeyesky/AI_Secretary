import re
from datetime import datetime

_TIME_FORMATS = ("%I:%M %p", "%I %p", "%H:%M")

_KEYWORDS = {
    "noon": "12:00 pm",
    "midday": "12:00 pm",
    "midnight": "12:00 am",
}

def _normalize(text: str) -> str:
    normalized = text.strip().lower().replace("p.m.", "pm").replace("a.m.", "am")
    for source, target in _KEYWORDS.items():
        normalized = normalized.replace(source, target)
    normalized = re.sub(r"(?<=\d)\s*(am|pm)\b", r" \1", normalized)
    return normalized.strip()


def parse_time(text: str, *, base: datetime | None = None) -> datetime:
    normalized = _normalize(text)
    anchor = base or datetime.now()

    for fmt in _TIME_FORMATS:
        try:
            parsed = datetime.strptime(normalized, fmt)
        except ValueError:
            continue
        return anchor.replace(
            hour=parsed.hour,
            minute=parsed.minute,
            second=0,
            microsecond=0,
        )

    raise ValueError(f"Could not parse time: {text!r}")
