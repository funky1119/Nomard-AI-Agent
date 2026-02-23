import yfinance as yf
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm(model="openai/gpt-4o")


def get_income_statement(ticker: str):
    """
    매출 및 수익성 분석을 위한 손익계산서를 조회합니다.

    이 도구는 최근 보고 기간 동안의 매출, 비용, 다양한 단계의 이익률을 포함한
    상세 손익계산서 데이터를 가져옵니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: Apple Inc.의 'AAPL')

    Returns:
        dict: 다음을 포함하는 딕셔너리:
            - ticker (str): 입력한 티커 심볼
            - success (bool): 작업 성공 여부 (성공 시 True)
            - income_statement (str): 다음 항목을 포함한 JSON 형식 손익계산서 데이터:
                * Total Revenue
                * Cost of Revenue
                * Gross Profit
                * Operating Expenses
                * Operating Income
                * EBITDA
                * Net Income
                * Earnings Per Share (EPS)

    Notes:
        - 일반적으로 최근 4개 분기 및 연간 기간 데이터를 포함
        - 모든 재무 수치는 회사의 보고 통화 기준
        - 매출 성장, 마진 추이, 수익성 분석에 유용

    Example:
        >>> get_income_statement('GOOGL')
        {
            'ticker': 'GOOGL',
            'success': True,
            'income_statement': '{"Total Revenue": {...}, "Net Income": {...}}'
        }
    """
    stock = yf.Ticker(ticker)
    # return stock.income_stmt.to_json()
    return {
        "ticker": ticker,
        "success": True,
        "income_statement": stock.income_stmt.to_json(),
    }


def get_balance_sheet(ticker: str):
    """
    재무 상태와 자본 구조 분석을 위한 재무상태표를 조회합니다.

    이 도구는 특정 시점의 자산, 부채, 자본 데이터를 포함한 재무상태표를 가져와
    재무 건전성과 자본 효율성에 대한 인사이트를 제공합니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: Apple Inc.의 'AAPL')

    Returns:
        dict: 다음을 포함하는 딕셔너리:
            - ticker (str): 입력한 티커 심볼
            - success (bool): 작업 성공 여부 (성공 시 True)
            - balance_sheet (str): 다음 항목을 포함한 JSON 형식 재무상태표 데이터:
                * Current Assets (cash, receivables, inventory)
                * Non-Current Assets (PP&E, intangibles, investments)
                * Current Liabilities (payables, short-term debt)
                * Non-Current Liabilities (long-term debt, deferred items)
                * Total Shareholders' Equity
                * Working Capital components

    Notes:
        - 분기말/연말 기준 재무 상태 스냅샷 제공
        - 유동성 비율(유동비율, 당좌비율) 계산에 필수
        - 부채 수준, 자산 효율성, 장부가치 평가에 활용
        - 모든 값은 회사의 보고 통화 기준

    Example:
        >>> get_balance_sheet('AMZN')
        {
            'ticker': 'AMZN',
            'success': True,
            'balance_sheet': '{"Total Assets": {...}, "Total Liabilities": {...}}'
        }
    """
    stock = yf.Ticker(ticker)
    # return stock.balance_sheet.to_json()
    return {
        "ticker": ticker,
        "success": True,
        "balance_sheet": stock.balance_sheet.to_json(),
    }


def get_cash_flow(ticker: str):
    """
    현금 창출력과 자본 배분 분석을 위한 현금흐름표를 조회합니다.

    이 도구는 영업/투자/재무 활동 전반에서 회사가 현금을 어떻게 창출하고 사용하는지
    보여주는 상세 현금흐름 데이터를 가져와 재무 지속 가능성과 성장 여력을 평가합니다.

    Args:
        ticker (str): 주식 티커 심볼 (예: Apple Inc.의 'AAPL')

    Returns:
        dict: 다음을 포함하는 딕셔너리:
            - ticker (str): 입력한 티커 심볼
            - success (bool): 작업 성공 여부 (성공 시 True)
            - cash_flow (str): 다음 항목을 포함한 JSON 형식 현금흐름표 데이터:
                * Operating Cash Flow (cash from core business)
                * Capital Expenditures (CapEx)
                * Free Cash Flow (Operating CF - CapEx)
                * Investing Activities (acquisitions, investments)
                * Financing Activities (debt, dividends, buybacks)
                * Net Change in Cash

    Notes:
        - 영업현금흐름은 본업의 현금 창출력을 보여줌
        - 잉여현금흐름은 주주환원/성장에 활용 가능한 현금을 의미
        - 투자활동 현금흐름의 음수는 성장 투자를 의미하는 경우가 많음
        - 재무활동 현금흐름은 자본 구조 의사결정을 보여줌
        - 배당 지속 가능성 및 성장 자금 평가에 중요

    Example:
        >>> get_cash_flow('META')
        {
            'ticker': 'META',
            'success': True,
            'cash_flow': '{"Operating Cash Flow": {...}, "Free Cash Flow": {...}}'
        }
    """
    stock = yf.Ticker(ticker)
    # return stock.balance_sheet.to_json()
    return {
        "ticker": ticker,
        "success": True,
        "cash_flow": stock.cash_flow.to_json(),
    }


financial_analyst = Agent(
    name="FinancialAnalyst",
    model=MODEL,
    description="손익계산서, 재무상태표, 현금흐름표를 포함한 상세 재무제표를 분석합니다",
    instruction="""
    당신은 심층 재무제표 분석을 수행하는 재무 애널리스트입니다. 역할은 다음과 같습니다.
    
    1. **손익 분석**: get_income_statement()로 매출, 수익성, 마진을 분석
    2. **재무상태표 분석**: get_balance_sheet()로 자산, 부채, 재무 상태를 점검
    3. **현금흐름 분석**: get_cash_flow()로 현금 창출력과 자본 배분을 평가
    
    **사용 가능한 재무 도구:**
    - **get_income_statement(ticker)**: 매출, 이익률, 수익성 분석
    - **get_balance_sheet(ticker)**: 자산, 부채, 자본, 재무 건전성 지표
    - **get_cash_flow(ticker)**: 영업현금흐름, 잉여현금흐름, 자본적지출
    
    종합 재무제표 데이터를 활용해 기업의 재무 건전성과 성과를 분석하세요.
    기업의 재무 체력을 보여주는 핵심 비율, 추세, 지표에 집중하세요.
    """,
    tools=[
        get_income_statement,
        get_balance_sheet,
        get_cash_flow,
    ],
)
