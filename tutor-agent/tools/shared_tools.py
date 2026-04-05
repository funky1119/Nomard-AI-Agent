import re
import os
from langgraph.types import Command
from langchain_core.tools import tool
from firecrawl import FirecrawlApp

@tool
def transfer_to_agent(agent_name: str):
    """
    지정된 에이전트로 전달합니다.

    Args:
        agent_name: 전달할 에이전트 이름. 예: 'quiz_agent', 'teacher_agent', 'feynman_agent'
    """
    return Command(
        goto=agent_name,
        graph=Command.PARENT,
        update={
            "current_agent": agent_name,
        },
    )

@tool
def web_search_tool(query: str):
    """
    웹 검색 도구입니다.
    Args:
        query: str
            웹에서 검색할 질의입니다.
    반환값:
        웹사이트 본문을 Markdown 형식으로 정리한 검색 결과 목록을 반환합니다.
    """
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    try:
        response = app.search(
            query=query,
            limit=5,
            scrape_options={
                "formats": ["markdown"],
            },
        )
    except Exception as exc:
        return f"도구 사용 중 오류가 발생했습니다: {exc}"

    cleaned_chunks = []

    for source_name in ("web", "news", "images"):
        results = getattr(response, source_name, None) or []

        for result in results:
            if hasattr(result, "model_dump"):
                result_dict = result.model_dump()
            elif isinstance(result, dict):
                result_dict = result
            else:
                continue

            title = result_dict.get("title") or ""
            url = result_dict.get("url") or result_dict.get("image_url") or ""
            markdown = (
                result_dict.get("markdown")
                or result_dict.get("snippet")
                or result_dict.get("description")
                or ""
            )

            if not markdown:
                continue

            cleaned = re.sub(r"\\+|\n+", "", markdown).strip()
            cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

            cleaned_chunks.append(
                {
                    "title": title,
                    "url": url,
                    "markdown": cleaned,
                }
            )

    if not cleaned_chunks:
        return "검색 결과는 있었지만 추출 가능한 본문이 없었습니다."

    return cleaned_chunks
