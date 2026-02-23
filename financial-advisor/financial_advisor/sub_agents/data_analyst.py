import yfinance as yf
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm


MODEL = LiteLlm(model="openai/gpt-4o")


def get_company_info(ticker: str) -> str:
    """
    주어진 주식 티커의 기본 회사 정보를 조회합니다.

    이 도구는 Yahoo Finance에서 회사의 정식 명칭, 산업 분류, 섹터 분류 등
    핵심 회사 정보를 가져옵니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: Apple Inc.의 'AAPL')

    Returns:
        dict: 다음을 포함하는 딕셔너리:
            - ticker (str): 입력한 티커 심볼
            - success (bool): 작업 성공 여부 (성공 시 True)
            - company_name (str): 회사의 전체 법인명
            - industry (str): 세부 산업 분류
            - sector (str): 상위 섹터 분류

    Example:
        >>> get_company_info('MSFT')
        {
            'ticker': 'MSFT',
            'success': True,
            'company_name': 'Microsoft Corporation',
            'industry': 'Software - Infrastructure',
            'sector': 'Technology'
        }
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "success": True,
        "company_name": info.get("longName", "NA"),
        "industry": info.get("industry", "NA"),
        "sector": info.get("sector", "NA"),
    }


def get_stock_price(ticker: str, period: str) -> str:
    """
    주어진 티커의 과거 주가 데이터와 현재 거래 가격을 조회합니다.

    이 도구는 지정한 기간의 시가/고가/저가/종가/거래량을 포함한 과거 가격 데이터와
    현재 시장 가격을 함께 가져옵니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: Apple Inc.의 'AAPL')
        period (str): 과거 데이터 조회 기간. 사용 가능한 옵션:
            - '1d': 1일
            - '5d': 5일
            - '1mo': 1개월 (기본값)
            - '3mo': 3개월
            - '6mo': 6개월
            - '1y': 1년
            - '2y': 2년
            - '5y': 5년
            - '10y': 10년
            - 'ytd': 연초 이후(YTD)
            - 'max': 사용 가능한 최대 기간

    Returns:
        dict: 다음을 포함하는 딕셔너리:
            - ticker (str): 입력한 티커 심볼
            - success (bool): 작업 성공 여부 (성공 시 True)
            - history (str): OHLCV 형식의 JSON 과거 가격 데이터
            - current_price (float): 현재 주식 시장 가격

    Example:
        >>> get_stock_price('TSLA', '3mo')
        {
            'ticker': 'TSLA',
            'success': True,
            'history': '{"Open": {...}, "High": {...}, ...}',
            'current_price': 245.67
        }
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    history = stock.history(period=period)
    return {
        "ticker": ticker,
        "success": True,
        "history": history.to_json(),
        "current_price": info.get("currentPrice"),
    }


def get_financial_metrics(ticker: str) -> str:
    """
    주식 분석에 필요한 핵심 재무 지표와 밸류에이션 비율을 조회합니다.

    이 도구는 회사의 밸류에이션, 수익성, 배당 정책, 시장 위험 특성을 평가하는 데
    도움이 되는 주요 재무 지표를 가져옵니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: Apple Inc.의 'AAPL')

    Returns:
        dict: 다음을 포함하는 딕셔너리:
            - ticker (str): 입력한 티커 심볼
            - success (bool): 작업 성공 여부 (성공 시 True)
            - market_cap (float): USD 기준 총 시가총액
            - pe_ratio (float): 후행 주가수익비율(P/E, 주가/주당순이익)
            - dividend_yield (float): 연간 배당수익률 (0.02 = 2%)
            - beta (float): 시장 대비 변동성을 나타내는 베타 계수

    Notes:
        - Market Cap: 회사의 총 가치(주식 수 * 주가)를 의미
        - P/E Ratio: 낮으면 저평가 가능성, 높으면 성장 기대 반영 가능성
        - Dividend Yield: 주가 대비 연간 배당 비율
        - Beta: 1 미만은 시장보다 낮은 변동성, 1 초과는 높은 변동성

    Example:
        >>> get_financial_metrics('JNJ')
        {
            'ticker': 'JNJ',
            'success': True,
            'market_cap': 385000000000,
            'pe_ratio': 15.2,
            'dividend_yield': 0.031,
            'beta': 0.65
        }
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "success": True,
        "market_cap": info.get("marketCap", "NA"),
        "pe_ratio": info.get("trailingPE", "NA"),
        "dividend_yield": info.get("dividendYield", "NA"),
        "beta": info.get("beta", "NA"),
    }


data_analyst = LlmAgent(
    name="DataAnalyst",
    model=MODEL,
    description="여러 특화 도구를 사용해 기본 주식 시장 데이터를 수집하고 분석합니다",
    instruction="""
    당신은 여러 특화 도구를 사용해 주식 정보를 수집하는 데이터 애널리스트입니다.
    
    1. **get_company_info(ticker)** - 회사 정보 확인 (이름, 섹터, 산업)
    2. **get_stock_price(ticker, period)** - 현재 가격 및 거래 범위 조회
    3. **get_financial_metrics(ticker)** - 핵심 재무 비율 확인
    
    여러 도구를 조합해 다양한 유형의 데이터를 수집하세요.
    각 도구가 제공하는 정보를 설명하고, 결과를 명확하게 정리해 제시하세요.
    """,
    tools=[
        get_company_info,
        get_stock_price,
        get_financial_metrics,
    ],
)
