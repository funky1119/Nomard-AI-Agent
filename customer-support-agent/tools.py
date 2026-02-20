import streamlit as st
from agents import function_tool, AgentHooks, Agent, Tool, RunContextWrapper
from models import UserAccountContext
import random
from datetime import datetime, timedelta


# =============================================================================
# 기술 지원 도구
# =============================================================================


@function_tool
def run_diagnostic_check(
    context: UserAccountContext, product_name: str, issue_description: str
) -> str:
    """
    고객 제품의 잠재적 문제를 파악하기 위해 진단 점검을 실행합니다.

    Args:
        product_name: 문제가 발생한 제품명
        issue_description: 문제 설명
    """
    diagnostics = [
        "✅ 서버 연결 상태: 정상",
        "✅ API 엔드포인트: 응답 정상",
        "⚠️  캐시 메모리: 85% 사용 중 (정리 권장)",
        "✅ 데이터베이스 연결: 안정적",
        "⚠️  마지막 업데이트: 7일 전 (업데이트 가능)",
    ]

    return f"🔍 {product_name} 진단 결과:\n" + "\n".join(diagnostics)


@function_tool
def provide_troubleshooting_steps(context: UserAccountContext, issue_type: str) -> str:
    """
    자주 발생하는 문제에 대한 단계별 문제 해결 안내를 제공합니다.

    Args:
        issue_type: 문제 유형 (connection, login, performance, crash 등)
    """
    steps_map = {
        "connection": [
            "1. 인터넷 연결 상태를 확인하세요",
            "2. 브라우저 캐시와 쿠키를 삭제하세요",
            "3. 브라우저 확장 프로그램을 잠시 비활성화하세요",
            "4. 시크릿/프라이빗 모드에서 다시 시도하세요",
            "5. 라우터/모뎀을 재시작하세요",
        ],
        "login": [
            "1. 사용자명과 비밀번호를 확인하세요",
            "2. Caps Lock이 꺼져 있는지 확인하세요",
            "3. 브라우저 캐시를 삭제하세요",
            "4. 필요 시 비밀번호 재설정을 진행하세요",
            "5. VPN을 잠시 비활성화하세요",
        ],
        "performance": [
            "1. 불필요한 브라우저 탭을 닫으세요",
            "2. 브라우저 캐시를 삭제하세요",
            "3. 사용 가능한 RAM/저장 공간을 확인하세요",
            "4. 브라우저를 최신 버전으로 업데이트하세요",
            "5. 애플리케이션을 재시작하세요",
        ],
        "crash": [
            "1. 최신 버전으로 업데이트하세요",
            "2. 애플리케이션을 재시작하세요",
            "3. 시스템 요구사항을 확인하세요",
            "4. 충돌 가능 소프트웨어를 비활성화하세요",
            "5. 안전 모드로 실행해 보세요",
        ],
    }

    steps = steps_map.get(
        issue_type.lower(),
        [
            "1. 애플리케이션을 재시작하세요",
            "2. 업데이트 가능 여부를 확인하세요",
            "3. 오류 상세 정보와 함께 지원팀에 문의하세요",
        ],
    )

    context.add_troubleshooting_step(f"{issue_type} 문제 해결 단계 제공")
    return f"🛠️ {issue_type} 문제 해결 단계:\n" + "\n".join(steps)


@function_tool
def escalate_to_engineering(
    context: UserAccountContext, issue_summary: str, priority: str = "medium"
) -> str:
    """
    기술 이슈를 엔지니어링 팀으로 에스컬레이션합니다.

    Args:
        issue_summary: 기술 이슈 요약
        priority: 우선순위 (low, medium, high, critical)
    """
    ticket_id = f"ENG-{random.randint(10000, 99999)}"

    return f"""
🚀 엔지니어링 팀으로 이슈가 에스컬레이션되었습니다
📋 티켓 ID: {ticket_id}
⚡ 우선순위: {priority.upper()}
📝 요약: {issue_summary}
🕐 예상 응답 시간: {2 if context.is_premium_customer() else 4}시간
    """.strip()


# =============================================================================
# 결제 지원 도구
# =============================================================================


@function_tool
def lookup_billing_history(context: UserAccountContext, months_back: int = 6) -> str:
    """
    고객의 결제/청구 이력과 결제 기록을 조회합니다.

    Args:
        months_back: 조회할 과거 개월 수 (기본값 6)
    """
    payments = []
    for i in range(months_back):
        date = datetime.now() - timedelta(days=30 * i)
        amount = random.choice([29.99, 49.99, 99.99])
        status = random.choice(["결제 완료", "결제 완료", "결제 완료", "실패"])
        payments.append(f"• {date.strftime('%Y-%m')}: ${amount} - {status}")

    return f"💳 결제 이력 (최근 {months_back}개월):\n" + "\n".join(payments)


@function_tool
def process_refund_request(
    context: UserAccountContext, refund_amount: float, reason: str
) -> str:
    """
    고객의 환불 요청을 처리합니다.

    Args:
        refund_amount: 환불 금액
        reason: 환불 사유
    """
    processing_days = 3 if context.is_premium_customer() else 5
    refund_id = f"REF-{random.randint(100000, 999999)}"

    return f"""
✅ 환불 요청이 처리되었습니다
🔗 환불 ID: {refund_id}
💰 금액: ${refund_amount}
📝 사유: {reason}
⏱️ 처리 기간: 영업일 기준 {processing_days}일
💳 환불 금액은 기존 결제 수단으로 반환됩니다
    """.strip()


@function_tool
def update_payment_method(context: UserAccountContext, payment_type: str) -> str:
    """
    고객의 결제 수단 변경을 지원합니다.

    Args:
        payment_type: 결제 수단 유형 (credit_card, paypal, bank_transfer)
    """
    return f"""
💳 결제 수단 변경이 시작되었습니다
📋 유형: {payment_type.replace("_", " ").title()}
🔒 보안 링크 발송 대상: {context.email}
⏰ 링크 만료 시간: 24시간
✅ 현재 서비스는 중단되지 않습니다
    """.strip()


@function_tool
def apply_billing_credit(
    context: UserAccountContext, credit_amount: float, reason: str
) -> str:
    """
    결제 이슈 보상 또는 크레딧 지급을 적용합니다.

    Args:
        credit_amount: 적용할 크레딧 금액
        reason: 크레딧 지급 사유
    """
    return f"""
🎁 계정 크레딧이 적용되었습니다
💰 크레딧 금액: ${credit_amount}
📝 사유: {reason}
⚡ 적용 계정: {context.customer_id}
📧 확인 메일 발송 대상: {context.email}
    """.strip()


# =============================================================================
# 주문 관리 도구
# =============================================================================


@function_tool
def lookup_order_status(context: UserAccountContext, order_number: str) -> str:
    """
    주문의 현재 상태와 상세 정보를 조회합니다.

    Args:
        order_number: 고객 주문 번호
    """
    statuses = ["처리중", "배송됨", "배송중", "배송완료"]
    current_status = random.choice(statuses)

    tracking_number = f"1Z{random.randint(100000, 999999)}"
    estimated_delivery = datetime.now() + timedelta(days=random.randint(1, 5))

    return f"""
📦 주문 상태: {order_number}
🏷️ 상태: {current_status}
🚚 운송장 번호: {tracking_number}
📅 예상 배송일: {estimated_delivery.strftime("%Y-%m-%d")}
📍 배송 대상: {context.email}
    """.strip()


@function_tool
def initiate_return_process(
    context: UserAccountContext, order_number: str, return_reason: str, items: str
) -> str:
    """
    주문 반품 절차를 시작합니다.

    Args:
        order_number: 반품할 주문 번호
        return_reason: 반품 사유
        items: 반품 품목
    """
    return_id = f"RET-{random.randint(100000, 999999)}"
    return_label_fee = 0 if context.is_premium_customer() else 5.99

    return f"""
📦 반품이 접수되었습니다
🔗 반품 ID: {return_id}
📋 주문 번호: {order_number}
📝 반품 품목: {items}
💰 반품 라벨 수수료: ${return_label_fee}
📧 반품 라벨 발송 대상: {context.email}
⏰ 반품 가능 기간: 30일
    """.strip()


@function_tool
def schedule_redelivery(
    context: UserAccountContext, tracking_number: str, preferred_date: str
) -> str:
    """
    배송 실패 건의 재배송 일정을 등록합니다.

    Args:
        tracking_number: 택배 운송장 번호
        preferred_date: 고객 희망 배송일
    """
    return f"""
🚚 재배송 일정이 등록되었습니다
📦 운송장 번호: {tracking_number}
📅 신규 배송일: {preferred_date}
🏠 배송지 확인: {context.email}
📞 배송 30분 전에 기사님이 연락드립니다
    """.strip()


@function_tool
def expedite_shipping(context: UserAccountContext, order_number: str) -> str:
    """
    주문 배송 속도를 상향합니다 (프리미엄 고객 전용).

    Args:
        order_number: 빠른 배송으로 전환할 주문 번호
    """
    if not context.is_premium_customer():
        return "❌ 빠른 배송 업그레이드는 프리미엄 멤버십이 필요합니다"

    return f"""
⚡ 배송이 빠른 옵션으로 전환되었습니다
📦 주문 번호: {order_number}
🚀 적용 옵션: 익일 배송
💰 추가 요금 없음 (프리미엄 혜택)
📧 변경된 배송 정보 발송 대상: {context.email}
    """.strip()


# =============================================================================
# 계정 관리 도구
# =============================================================================


@function_tool
def reset_user_password(context: UserAccountContext, email: str) -> str:
    """
    고객 이메일로 비밀번호 재설정 안내를 전송합니다.

    Args:
        email: 재설정 안내를 보낼 이메일 주소
    """
    reset_token = f"RST-{random.randint(100000, 999999)}"

    return f"""
🔐 비밀번호 재설정이 시작되었습니다
📧 재설정 링크 발송 대상: {email}
🔗 재설정 토큰: {reset_token}
⏰ 링크 만료 시간: 1시간
🛡️ 보안을 위해 링크는 1회만 사용할 수 있습니다
    """.strip()


@function_tool
def enable_two_factor_auth(context: UserAccountContext, method: str = "app") -> str:
    """
    고객의 2단계 인증 설정을 지원합니다.

    Args:
        method: 2FA 방식 (app, sms, email)
    """
    setup_code = f"2FA-{random.randint(100000, 999999)}"

    return f"""
🔒 2단계 인증 설정
📱 방식: {method.upper()}
🔑 설정 코드: {setup_code}
📧 안내 발송 대상: {context.email}
⚡ 보안 강화가 활성화되었습니다
    """.strip()


@function_tool
def update_account_email(
    context: UserAccountContext, old_email: str, new_email: str
) -> str:
    """
    계정 이메일 주소 변경을 처리합니다.

    Args:
        old_email: 현재 이메일 주소
        new_email: 새 이메일 주소
    """
    verification_code = f"VER-{random.randint(100000, 999999)}"

    return f"""
📧 이메일 변경 요청이 접수되었습니다
📤 기존 주소: {old_email}
📥 새 주소: {new_email}
🔐 인증 코드: {verification_code}
⏰ 코드 만료 시간: 30분
✅ 인증 완료 후 변경이 적용됩니다
    """.strip()


@function_tool
def deactivate_account(
    context: UserAccountContext, reason: str, feedback: str = ""
) -> str:
    """
    계정 비활성화 요청을 처리합니다.

    Args:
        reason: 계정 비활성화 사유
        feedback: 고객 추가 의견 (선택)
    """
    return f"""
⚠️ 계정 비활성화가 시작되었습니다
👤 계정: {context.customer_id}
📝 사유: {reason}
💬 의견: {feedback if feedback else "제공되지 않음"}
⏰ 24시간 후 계정이 비활성화됩니다
🔄 30일 이내 재활성화할 수 있습니다
📧 확인 메일 발송 대상: {context.email}
    """.strip()


@function_tool
def export_account_data(context: UserAccountContext, data_types: str) -> str:
    """
    고객 계정 데이터 내보내기를 생성합니다.

    Args:
        data_types: 내보낼 데이터 유형 (profile, orders, billing 등)
    """
    export_id = f"EXP-{random.randint(100000, 999999)}"

    return f"""
📊 데이터 내보내기 요청이 접수되었습니다
🔗 내보내기 ID: {export_id}
📋 데이터 유형: {data_types}
⏱️ 처리 시간: 2~4시간
📧 다운로드 링크 발송 대상: {context.email}
🔒 링크 만료 기간: 7일
    """.strip()


class AgentToolUsageLoggingHooks(AgentHooks):
    async def on_tool_start(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
        tool: Tool,
    ):
        with st.sidebar:
            st.write(f"🔧 **{agent.name}** 도구 시작: `{tool.name}`")

    async def on_tool_end(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
        tool: Tool,
        result: str,
    ):
        with st.sidebar:
            st.write(f"🔧 **{agent.name}** 도구 사용: `{tool.name}`")
            st.code(result)

    async def on_handoff(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
        source: Agent[UserAccountContext],
    ):
        with st.sidebar:
            st.write(f"🔄 핸드오프: **{source.name}** → **{agent.name}**")

    async def on_start(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
    ):
        with st.sidebar:
            st.write(f"🚀 **{agent.name}** 활성화")

    async def on_end(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
        output,
    ):
        with st.sidebar:
            st.write(f"🏁 **{agent.name}** 완료")
