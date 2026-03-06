from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prompt import (
    TRAVEL_ADVISOR_DESCRIPTION,
    TRAVEL_ADVISOR_INSTRUCTION,
)
from google.adk.tools.tool_context import ToolContext

MODEL = LiteLlm(model="openai/gpt-4o")


async def get_weather(tool_context: ToolContext, location: str):
    """특정 지역의 현재 날씨 정보를 반환합니다."""
    # 더미 구현 - 모의 데이터를 반환합니다.
    return {
        "location": location,
        "temperature": "22°C",
        "condition": "구름 조금",
        "humidity": "65%",
        "wind": "12 km/h",
        "forecast": "하루 종일 온화한 날씨에 가끔 구름이 낄 것으로 예상됩니다",
    }


async def get_exchange_rate(
    tool_context: ToolContext, from_currency: str, to_currency: str, amount: float
):
    """두 통화 간 환율 정보를 반환합니다.
    인자는 항상 from_currency 문자열, to_currency 문자열, amount 실수여야 합니다.
    """
    # 더미 구현 - 모의 데이터를 반환합니다.
    mock_rates = {
        ("USD", "EUR"): 0.92,
        ("USD", "GBP"): 0.79,
        ("USD", "JPY"): 149.50,
        ("USD", "KRW"): 1325.00,
        ("EUR", "USD"): 1.09,
        ("EUR", "GBP"): 0.86,
        ("GBP", "USD"): 1.27,
        ("JPY", "USD"): 0.0067,
        ("KRW", "USD"): 0.00075,
    }

    rate = mock_rates.get((from_currency, to_currency), 1.0)
    converted_amount = amount * rate

    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "exchange_rate": rate,
        "converted_amount": converted_amount,
        "timestamp": "2024-03-15 10:30:00 UTC",
    }


async def get_local_attractions(
    tool_context: ToolContext, location: str, category: str = "all"
):
    """특정 지역의 인기 관광지와 주요 명소 정보를 반환합니다."""
    # 더미 구현 - 모의 데이터를 반환합니다.
    attractions = {
        "Paris": [
            {
                "name": "Eiffel Tower",
                "type": "landmark",
                "rating": 4.8,
                "description": "상징적인 철제 격자 구조의 탑",
            },
            {
                "name": "Louvre Museum",
                "type": "museum",
                "rating": 4.7,
                "description": "세계 최대 규모의 미술관",
            },
            {
                "name": "Arc de Triomphe",
                "type": "monument",
                "rating": 4.6,
                "description": "역사적인 개선문",
            },
            {
                "name": "Notre-Dame",
                "type": "cathedral",
                "rating": 4.5,
                "description": "중세 가톨릭 대성당",
            },
            {
                "name": "Sacré-Cœur",
                "type": "basilica",
                "rating": 4.4,
                "description": "로마네스크-비잔틴 양식의 바실리카",
            },
        ],
        "Tokyo": [
            {
                "name": "Tokyo Tower",
                "type": "landmark",
                "rating": 4.5,
                "description": "전파 송출과 전망 기능을 갖춘 타워",
            },
            {
                "name": "Senso-ji",
                "type": "temple",
                "rating": 4.6,
                "description": "유서 깊은 불교 사찰",
            },
            {
                "name": "Shibuya Crossing",
                "type": "landmark",
                "rating": 4.4,
                "description": "세계적으로 유명한 혼잡한 횡단보도",
            },
            {
                "name": "Meiji Shrine",
                "type": "shrine",
                "rating": 4.7,
                "description": "메이지 천황을 기리는 신토 신사",
            },
            {
                "name": "Tokyo Skytree",
                "type": "tower",
                "rating": 4.6,
                "description": "방송 송출과 전망 기능을 갖춘 타워",
            },
        ],
        "default": [
            {
                "name": "City Center",
                "type": "area",
                "rating": 4.2,
                "description": "도심 중심 지역",
            },
            {
                "name": "Historical Museum",
                "type": "museum",
                "rating": 4.3,
                "description": "지역 역사와 문화를 다루는 박물관",
            },
            {
                "name": "Central Park",
                "type": "park",
                "rating": 4.1,
                "description": "대표적인 공공 공원",
            },
            {
                "name": "Old Town",
                "type": "district",
                "rating": 4.4,
                "description": "전통 건축물이 남아 있는 역사 지구",
            },
            {
                "name": "Local Market",
                "type": "market",
                "rating": 4.0,
                "description": "전통적인 현지 시장",
            },
        ],
    }

    location_attractions = attractions.get(location, attractions["default"])

    if category != "all":
        location_attractions = [
            a for a in location_attractions if a["type"] == category
        ]

    return {
        "location": location,
        "category": category,
        "attractions": location_attractions,
        "total_count": len(location_attractions),
    }


travel_advisor_agent = Agent(
    name="TravelAdvisorAgent",
    description=TRAVEL_ADVISOR_DESCRIPTION,
    instruction=TRAVEL_ADVISOR_INSTRUCTION,
    tools=[
        get_weather,
        get_exchange_rate,
        get_local_attractions,
    ],
    model=MODEL,
)

root_agent = travel_advisor_agent
