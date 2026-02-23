from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools import web_search_tool


MODEL = LiteLlm(model="openai/gpt-4o")


news_analyst = Agent(
    name="NewsAnalyst",
    model=MODEL,
    description="웹 검색 도구를 사용해 실제 웹 콘텐츠를 검색하고 수집합니다.",
    instruction="""
    당신은 웹 도구를 사용해 최신 정보를 찾는 뉴스 분석 전문가입니다. 역할은 다음과 같습니다.
    
    1. **웹 검색**: web_search_tool()을 사용해 기업 관련 최신 뉴스를 찾습니다.
    3. **결과 요약**: 찾은 내용과 그 관련성을 설명합니다.
    
    **사용 가능한 웹 도구:**
    - **web_search_tool()**: 기업 뉴스 검색용 Firecrawl 웹 검색
    
    외부 API를 사용해 현재 정보를 위한 웹 콘텐츠를 검색하고 수집하세요.
    """,
    tools=[
        web_search_tool,
    ],
)
