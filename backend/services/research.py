import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import ResearchResult, ResearchSession, Source
from schemas import (
    AIResearchPayload,
    ChatResponse,
    ResearchResponse,
    ResearchResultDetail,
    ResearchResultSummary,
    SourceOut,
)
from services.ai import run_research
from services.cache import ResearchCache
from services.documents import document_cache_key, document_sources_for_session
from services.sessions import WorkspaceAccessError, add_message, get_or_create_session, get_recent_history
from services.sources import gather_sources, needs_search
from services.text import normalize_query, title_from_query


cache = ResearchCache()


def _payload_to_cache(payload: AIResearchPayload) -> dict:
    return payload.model_dump(mode="json")


def _payload_from_cache(data: dict) -> AIResearchPayload:
    return AIResearchPayload.model_validate(data)


def _persist_result(
    db: Session,
    session_id: str,
    query: str,
    payload: AIResearchPayload,
    cached: bool,
    latency_ms: int,
) -> ResearchResult:
    result = ResearchResult(
        session_id=session_id,
        query=query,
        answer=payload.answer,
        summary=payload.summary,
        confidence=payload.confidence,
        tools_used=payload.tools_used,
        cached=cached,
        latency_ms=latency_ms,
    )
    db.add(result)
    db.flush()

    for source in payload.sources:
        db.add(
            Source(
                research_result_id=result.id,
                title=source.title,
                url=source.url,
                snippet=source.snippet,
                source_type=source.source_type,
            )
        )

    db.commit()
    db.refresh(result)
    return result


def _source_strings(sources: list[SourceOut]) -> list[str]:
    values: list[str] = []
    for source in sources:
        label = source.title or source.source_type
        if source.url:
            label = f"{label} - {source.url}"
        if source.snippet:
            label = f"{label}: {source.snippet}"
        values.append(label)
    return values or ["FusionAI research synthesis"]


def _source_to_out(source: Source) -> SourceOut:
    return SourceOut(
        title=source.title,
        url=source.url,
        snippet=source.snippet,
        source_type=source.source_type,
    )


def result_to_summary(result: ResearchResult) -> ResearchResultSummary:
    return ResearchResultSummary(
        id=result.id,
        session_id=result.session_id,
        query=result.query,
        confidence=result.confidence,
        cached=result.cached,
        latency_ms=result.latency_ms,
        source_count=len(result.sources),
        created_at=result.created_at,
    )


def result_to_detail(result: ResearchResult) -> ResearchResultDetail:
    summary = result_to_summary(result)
    return ResearchResultDetail(
        **summary.model_dump(),
        answer=result.answer,
        summary=result.summary,
        tools_used=result.tools_used or [],
        citations=[_source_to_out(source) for source in result.sources],
    )


def get_research_result(db: Session, result_id: str, owner_id: str) -> ResearchResultDetail | None:
    result = db.get(ResearchResult, result_id)
    if not result or result.session.owner_id != owner_id:
        return None
    return result_to_detail(result)


def list_session_results(db: Session, session_id: str, owner_id: str) -> list[ResearchResultSummary] | None:
    session_exists = db.get(ResearchSession, session_id)
    if not session_exists or session_exists.owner_id != owner_id:
        return None
    stmt = (
        select(ResearchResult)
        .where(ResearchResult.session_id == session_id)
        .order_by(ResearchResult.created_at.desc())
    )
    return [result_to_summary(result) for result in db.scalars(stmt)]


def research_query(
    db: Session,
    query: str,
    session_id: str | None = None,
    owner_id: str = "anonymous",
) -> ResearchResponse:
    started = time.perf_counter()
    normalized_query = normalize_query(query)
    session = get_or_create_session(db, session_id, owner_id, title=title_from_query(query))
    add_message(db, session, "user", query)

    cached = False
    document_sources = document_sources_for_session(db, session.id)
    doc_key = document_cache_key(db, session.id)
    cache_mode = "research" if not doc_key else f"research:session:{session.id}:docs:{doc_key}"
    cached_payload = cache.get(normalized_query, mode=cache_mode)
    if cached_payload:
        payload = _payload_from_cache(cached_payload)
        cached = True
    else:
        history = get_recent_history(db, session.id)
        web_sources = gather_sources(query) if needs_search(query) else []
        sources = [*document_sources, *web_sources]
        payload = run_research(query, history, sources)
        if document_sources and "documents" not in payload.tools_used:
            payload.tools_used.append("documents")
        cache.set(normalized_query, _payload_to_cache(payload), mode=cache_mode)

    latency_ms = int((time.perf_counter() - started) * 1000)
    result = _persist_result(db, session.id, query, payload, cached, latency_ms)
    add_message(db, session, "assistant", payload.answer)

    return ResearchResponse(
        topic=query.title(),
        answer=payload.answer,
        summary=payload.summary,
        sources=_source_strings(payload.sources),
        tools_used=payload.tools_used,
        confidence=payload.confidence,
        cached=cached,
        latency_ms=latency_ms,
        session_id=session.id,
        result_id=result.id,
        citations=payload.sources,
    )


def chat_message(
    db: Session,
    message: str,
    session_id: str | None = None,
    owner_id: str = "anonymous",
) -> ChatResponse:
    response = research_query(db, message, session_id, owner_id)
    return ChatResponse(
        session_id=response.session_id or "",
        answer=response.answer or response.summary,
        sources=response.sources,
        tools_used=response.tools_used,
        confidence=response.confidence,
        cached=response.cached,
        latency_ms=response.latency_ms,
        result_id=response.result_id,
        citations=response.citations,
    )
