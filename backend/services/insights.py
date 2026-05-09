from collections import Counter

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models import Document, ResearchResult, ResearchSession


def get_insights(db: Session, workspace_id: str) -> dict:
    sessions = list(db.scalars(
        select(ResearchSession).where(ResearchSession.owner_id == workspace_id)
    ))
    session_ids = [s.id for s in sessions]
    total_sessions = len(sessions)

    if session_ids:
        results = list(db.scalars(
            select(ResearchResult).where(ResearchResult.session_id.in_(session_ids))
        ))
        total_documents = db.scalar(
            select(func.count(Document.id)).where(Document.session_id.in_(session_ids))
        ) or 0
    else:
        results = []
        total_documents = 0

    total_queries = len(results)

    confidence_breakdown: dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    tool_counter: Counter = Counter()
    cache_hits = 0
    total_latency = 0

    for r in results:
        conf = (r.confidence or "medium").lower()
        if conf in confidence_breakdown:
            confidence_breakdown[conf] += 1
        if r.tools_used:
            for tool in r.tools_used:
                tool_counter[str(tool).lower()] += 1
        if r.cached:
            cache_hits += 1
        total_latency += r.latency_ms or 0

    top_tools = [{"name": k, "count": v} for k, v in tool_counter.most_common(6)]
    avg_latency_ms = round(total_latency / total_queries, 1) if total_queries > 0 else 0.0
    cache_hit_rate = round(cache_hits / total_queries * 100, 1) if total_queries > 0 else 0.0

    session_result_counts: Counter = Counter(r.session_id for r in results)
    recent = sorted(sessions, key=lambda s: s.updated_at, reverse=True)[:5]
    recent_activity = [
        {
            "session_id": s.id,
            "title": s.title,
            "query_count": session_result_counts.get(s.id, 0),
            "updated_at": s.updated_at.isoformat(),
        }
        for s in recent
    ]

    return {
        "total_sessions": total_sessions,
        "total_queries": total_queries,
        "total_documents": total_documents,
        "confidence_breakdown": confidence_breakdown,
        "top_tools": top_tools,
        "avg_latency_ms": avg_latency_ms,
        "cache_hit_rate": cache_hit_rate,
        "recent_activity": recent_activity,
    }
