import streamlit as st
from agents import (
    Agent,
    RunContextWrapper,
    input_guardrail,
    Runner,
    GuardrailFunctionOutput,
    handoff,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters
from models import UserAccountContext, InputGuardRailOutput, HandoffData
from my_agents.billing_agent import billing_agent
from my_agents.account_agent import account_agent
from my_agents.order_agent import order_agent
from my_agents.technical_agent import technical_agent


input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="""
    사용자의 요청이 사용자 계정 정보, 결제 문의, 주문 정보 또는 기술 지원 이슈와 관련된 내용인지 확인하고, 주제에서 벗어나지 않았는지 판단하세요. 
    요청이 주제와 무관하다면 트립와이어(tripwire) 발동 사유를 반환하세요. 
    사용자와 가벼운 대화는 할 수 있으며, 특히 대화 초반에는 자연스러운 스몰토크가 가능합니다. 
    다만 사용자 계정 정보, 결제 문의, 주문 정보, 기술 지원 이슈와 관련되지 않은 요청에는 도움을 제공하지 마세요.
    """,
    output_type=InputGuardRailOutput,
)


@input_guardrail
async def off_topic_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
    input: str,
):
    result = await Runner.run(
        input_guardrail_agent,
        input,
        context=wrapper.context,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_off_topic,
    )


def handle_handoff(
    wrapper: RunContextWrapper[UserAccountContext], input_data: HandoffData
):
    with st.sidebar:
        st.write(f"""
            Handing off to {input_data.to_agent_name}
            Reason: {input_data.reason}
            Issue Type: {input_data.issue_type}
            Issue Description: {input_data.issue_description}
        """)


def make_handoff(agent):
    return handoff(
        agent=agent,
        on_handoff=handle_handoff,
        input_type=HandoffData,
        input_filter=handoff_filters.remove_all_tools,
    )


def dynamic_triage_agent_instructions(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
):
    if agent.name == "Triage Agent":
        # 분류를 위한 인스트럭션 생성
        return f"""
    사용자에게 한국어로 말하세요.

    {RECOMMENDED_PROMPT_PREFIX}


    당신은 고객 지원 상담 에이전트입니다. 고객의 사용자 계정, 결제, 주문, 기술 지원에 관한 질문만 도와줍니다.
    고객의 이름을 불러주세요.
    
    고객 이름: {wrapper.context.name}
    고객 이메일: {wrapper.context.email}
    고객 등급: {wrapper.context.tier}
    
    주요 업무: 고객의 문제를 분류하고, 적절한 전문 담당자에게 연결하세요.
    
    문제 분류 가이드:
    
    🔧 기술 지원 - 다음의 경우 여기로 연결:
    - 제품 작동 불량, 오류, 버그
    - 앱 충돌, 로딩 문제, 성능 저하
    - 기능 관련 질문, 사용법 안내
    - 연동 또는 설정 문제
    - "앱이 안 열려요", "오류 메시지가 떠요", "어떻게 하나요..."
    
    💰 결제 지원 - 다음의 경우 여기로 연결:
    - 결제 문제, 결제 실패, 환불
    - 구독 관련 질문, 플랜 변경, 해지
    - 청구서 문제, 결제 분쟁
    - 신용카드 변경, 결제 수단 변경
    - "이중 결제됐어요", "구독 해지해주세요", "환불 받고 싶어요"
    
    📦 주문 관리 - 다음의 경우 여기로 연결:
    - 주문 상태, 배송, 배달 관련 질문
    - 반품, 교환, 누락된 상품
    - 운송장 번호, 배송 문제
    - 상품 재고, 재주문
    - "제 주문 어디 있나요?", "반품하고 싶어요", "잘못된 상품이 왔어요"
    
    👤 계정 관리 - 다음의 경우 여기로 연결:
    - 로그인 문제, 비밀번호 재설정, 계정 접근
    - 프로필 수정, 이메일 변경, 계정 설정
    - 계정 보안, 2단계 인증
    - 계정 삭제, 데이터 내보내기 요청
    - "로그인이 안 돼요", "비밀번호를 잊었어요", "이메일을 변경하고 싶어요"
    
    분류 절차:
    1. 고객의 문제를 경청하세요.
    2. 분류가 명확하지 않으면 확인 질문을 하세요.
    3. 위 네 가지 카테고리 중 하나로 분류하세요.
    4. 연결 이유를 설명하세요: "[카테고리] 전문 담당자에게 연결해 드리겠습니다. [구체적인 문제]를 도와드릴 수 있습니다."
    5. 적절한 전문 에이전트에게 연결하세요.
    
    특별 처리 사항:
    - 프리미엄/엔터프라이즈 고객: 연결 시 우선 처리 대상임을 안내하세요.
    - 복합 문의: 가장 긴급한 문제부터 처리하고, 나머지는 후속 조치로 기록하세요.
    - 불명확한 문의: 연결 전에 1~2개의 확인 질문을 하세요.
    """


triage_agent = Agent(
    name="Triage Agent",
    instructions=dynamic_triage_agent_instructions,
    input_guardrails=[off_topic_guardrail],
    # tools=[
    #     technical_agent.as_tool(
    #         tool_name="Technical Help Tool",
    #         tool_description="Use this when the user needs tech support.",
    #     )
    # ],
    handoffs=[
        make_handoff(technical_agent),
        make_handoff(billing_agent),
        make_handoff(account_agent),
        make_handoff(order_agent),
    ],
)
