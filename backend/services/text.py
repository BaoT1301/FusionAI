import re


def normalize_query(query: str) -> str:
    cleaned = re.sub(r"\s+", " ", query.strip().lower())
    return cleaned


def title_from_query(query: str, max_length: int = 120) -> str:
    normalized = " ".join(query.strip().split())
    if len(normalized) <= max_length:
        return normalized
    return normalized[: max_length - 3].rstrip() + "..."
