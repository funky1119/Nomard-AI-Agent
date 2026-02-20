from agents import (
    Agent,
    output_guardrail,
    Runner,
    RunContextWrapper,
    GuardrailFunctionOutput,
)
from models import TechnicalOutputGuardRailOutput, UserAccountContext

technical_output_guardrail_agent = Agent(
    name="Technical Support Guardrail",
    instructions="""
    기술 지원 응답을 분석하여 아래 항목이 부적절하게 포함되어 있는지 확인하세요.

    - 결제/청구 정보 (결제, 환불, 요금, 구독)
    - 주문 정보 (배송, 운송장 추적, 배달, 반품)
    - 계정 관리 정보 (비밀번호, 이메일 변경, 계정 설정)

    기술 지원 에이전트는 오직 기술적 문제 해결, 진단, 제품 사용 지원만 제공해야 합니다.
    기술 지원 응답에 부적절한 내용이 포함된 필드는 모두 true로 반환하세요.
    """,
    output_type=TechnicalOutputGuardRailOutput,
)


@output_guardrail
async def technical_output_guardrail(
    wrapper: RunContextWrapper[UserAccountContext], agent: Agent, output: str
):
    result = await Runner.run(
        technical_output_guardrail_agent,
        output,
        context=wrapper.context,
    )

    validation = result.final_output

    triggered = (
        validation.contains_off_topic
        or validation.contains_billing_data
        or validation.contains_account_data
    )

    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )
