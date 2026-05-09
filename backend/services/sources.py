from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from config import get_settings
from schemas import SourceOut


def _trim(value: str | None, limit: int = 700) -> str:
    text = " ".join((value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _dedupe_sources(sources: list[SourceOut]) -> list[SourceOut]:
    seen: set[tuple[str, str | None]] = set()
    unique: list[SourceOut] = []
    for source in sources:
        key = (source.title.lower().strip(), source.url)
        if key in seen:
            continue
        seen.add(key)
        unique.append(source)
    return unique


def lookup_wikipedia(query: str, max_results: int) -> list[SourceOut]:
    if max_results <= 0:
        return []

    try:
        import wikipedia

        titles = wikipedia.search(query, results=max_results)
        sources: list[SourceOut] = []
        for title in titles:
            try:
                page = wikipedia.page(title, auto_suggest=False)
                # page.summary is already fetched by page(); no extra HTTP call needed
                sources.append(
                    SourceOut(
                        title=page.title,
                        url=page.url,
                        snippet=_trim(page.summary),
                        source_type="wikipedia",
                    )
                )
            except Exception:
                continue
        return sources
    except Exception:
        return []


def lookup_web(query: str, max_results: int) -> list[SourceOut]:
    if max_results <= 0:
        return []

    try:
        from ddgs import DDGS

        sources: list[SourceOut] = []
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            for item in results:
                title = item.get("title") or item.get("source") or "Web result"
                url = item.get("href") or item.get("url")
                snippet = item.get("body") or item.get("snippet") or ""
                sources.append(
                    SourceOut(
                        title=_trim(title, 180),
                        url=url,
                        snippet=_trim(snippet),
                        source_type="web",
                    )
                )
        return sources
    except Exception:
        return []


def gather_sources(query: str) -> list[SourceOut]:
    settings = get_settings()
    if not settings.source_lookup_enabled:
        return []

    # Run Wikipedia and web search concurrently — both are network I/O
    with ThreadPoolExecutor(max_workers=2) as pool:
        wiki_future = pool.submit(lookup_wikipedia, query, settings.wikipedia_results)
        web_future = pool.submit(lookup_web, query, settings.web_search_results)
        sources = [*wiki_future.result(), *web_future.result()]

    return _dedupe_sources(sources)


def source_context(sources: list[SourceOut]) -> str:
    if not sources:
        return "No external source context was available."

    blocks: list[str] = []
    for index, source in enumerate(sources, start=1):
        url = f"\nURL: {source.url}" if source.url else ""
        blocks.append(
            f"{index}. {source.title} ({source.source_type}){url}\nSnippet: {source.snippet}"
        )
    return "\n\n".join(blocks)
