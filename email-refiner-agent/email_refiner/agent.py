from google.adk.agents import Agent, LoopAgent
from google.adk.models.lite_llm import LiteLlm

from .prompt import (
    EMAIL_OPTIMIZER_DESCRIPTION,
    TONE_STYLIST_DESCRIPTION,
    CLARITY_EDITOR_DESCRIPTION,
    LITERARY_CRITIC_DESCRIPTION,
    EMAIL_SYNTHESIZER_DESCRIPTION,
    PERSUASION_STRATEGIST_DESCRIPTION,
    TONE_STYLIST_INSTRUCTION,
    CLARITY_EDITOR_INSTRUCTION,
    LITERARY_CRITIC_INSTRUCTION,
    EMAIL_SYNTHESIZER_INSTRUCTION,
    PERSUASION_STRATEGIST_INSTRUCTION,
)
from google.adk.tools.tool_context import ToolContext

MODEL = LiteLlm(model="openai/gpt-4o-mini")

# 이메일 초안의 모호함과 군더더기를 제거해 명확성과 간결함을 높이는 Agent
clarity_agent = Agent(
    name="ClarityEditorAgent",
    description=CLARITY_EDITOR_DESCRIPTION,
    instruction=CLARITY_EDITOR_INSTRUCTION,
    output_key="clarity_output",
    model=MODEL
)

# 명확해진 이메일의 톤을 따뜻하고 자신감 있으며 전문적으로 다듬는 Agent
tone_stylist_agent = Agent(
    name="ToneStylistAgent",
    description=TONE_STYLIST_DESCRIPTION,
    instruction=TONE_STYLIST_INSTRUCTION,
    output_key="tone_output",
    model=MODEL
)

# 톤이 다듬어진 이메일의 설득력과 행동 유도 표현을 강화하는 Agent
persuation_agent = Agent(
    name="PersuationAgent",
    description=PERSUASION_STRATEGIST_DESCRIPTION,
    instruction=PERSUASION_STRATEGIST_INSTRUCTION,
    output_key="persuasion_output",
    model=MODEL
)

# 명확성, 톤, 설득력 개선본을 통합해 최종 이메일 초안을 만드는 Agent
email_synthesizer_agent = Agent(
    name="EmailSynthesizerAgent",
    description=EMAIL_SYNTHESIZER_DESCRIPTION,
    instruction=EMAIL_SYNTHESIZER_INSTRUCTION,
    output_key="synthesized_output",
    model=MODEL
)

def escalate_email_complete(tool_context: ToolContext):
    """이메일이 괜찮을 때만 이 tool을 사용하세요."""
    # Roop 종료
    tool_context.actions.escalate = True
    return "이메일 최적화 완료"


# 통합된 이메일이 실무 수준의 품질 기준을 충족하는지 최종 검토하는 Agent
literary_critic_agent = Agent(
    name="LiteraryCriticAgent",
    description=LITERARY_CRITIC_DESCRIPTION,
    instruction=LITERARY_CRITIC_INSTRUCTION,
    tools=[escalate_email_complete], 
    model=MODEL
)

email_refiner_agent = LoopAgent(
    name="EmailRefinerAgent",
    max_iterations=50,
    description=EMAIL_OPTIMIZER_DESCRIPTION,    
    sub_agents=[
        clarity_agent,
        tone_stylist_agent,
        persuation_agent,
        email_synthesizer_agent,
        literary_critic_agent,
    ]
)

root_agent = email_refiner_agent
