"""Utilitarios centrais para manipulacao de PDF."""
from __future__ import annotations

from collections.abc import Iterable


def parse_page_selection(selection: str, total_pages: int) -> list[int]:
    """Converte uma selecao como '1-3, 5' em indices zero-based."""
    if not selection.strip():
        return list(range(total_pages))

    result: list[int] = []
    for token in selection.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            left, right = token.split("-", 1)
            start, end = int(left), int(right)
            if start > end:
                start, end = end, start
            for page in range(start, end + 1):
                if 1 <= page <= total_pages:
                    result.append(page - 1)
        else:
            page = int(token)
            if 1 <= page <= total_pages:
                result.append(page - 1)

    return list(dict.fromkeys(result))


def iter_chunks(items: Iterable, size: int):
    """Agrupa iteraveis em blocos de tamanho fixo."""
    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
