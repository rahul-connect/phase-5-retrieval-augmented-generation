"""Prepare natural-language queries for keyword retrieval."""

import re


def prepare_keyword_query(query: str) -> str:
    """Convert simple comparison questions into OR-style keyword queries."""

    query = query.strip()

    pattern = r"^compare\s+(.+?)\s+(?:and|vs\.?|versus)\s+(.+?)\??$"

    match = re.fullmatch(pattern, query, flags=re.IGNORECASE)

    if match is None:
        return query

    first_topic = match.group(1).strip()
    second_topic = match.group(2).strip()

    # Accept simple topic names, including multiword names,
    # digits, hyphens, periods, and plus signs.
    allowed_topic = r"[A-Za-z0-9][A-Za-z0-9 .+\-]*"

    if not re.fullmatch(allowed_topic, first_topic):
        return query

    if not re.fullmatch(allowed_topic, second_topic):
        return query

    # Reject explicit web-search operators inside topic names.
    if re.search(r"\bOR\b", first_topic, flags=re.IGNORECASE):
        return query

    if re.search(r"\bOR\b", second_topic, flags=re.IGNORECASE):
        return query

    return f"{first_topic} OR {second_topic}"