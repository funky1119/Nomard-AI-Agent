from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console

model = OpenAIChatCompletionClient(model="gpt-40-mini")

# 명확성 agent
clarity_agent = AssistantAgent(
    "ClarityAgent",
    model_client=model,
    system_message="""명확성과 간결함을 최우선으로 하는 전문 편집자로서, 저는 모호함과 중복을 제거하여 모든 문장을 군더더기 없이 명쾌하게 만드는 역할을 수행합니다.
    설득이나 감정적인 어조에 신경 쓰기보다, 메시지를 누구나 쉽고 빠르게 읽고 이해할 수 있도록 만드는 데 집중합니다.
    """,
)

# 톤(어조) agent : 이메일의 톤을 개선
tone_agent = AssistantAgent(
    "ToneAgent",
    model_client=model,
    system_message="""커뮤니케이션 코치로서, 저는 이메일의 정중함과 전문성을 유지하면서도 따뜻하고 자신감 넘치는 인간미가 느껴지도록 다듬어 드리는 역할을 맡습니다. 
    감정적인 공감대를 높이고 문장을 세련되게 다듬으며, 딱딱하거나 차갑게 느껴지는 표현 혹은 지나치게 가벼운 어조를 상황에 맞게 조정해 드릴 것입니다.
    """,
)

# 설득 agent : 이메일을 더 설득력 있게
persuasion_agent = AssistantAgent(
    "PersuasionAgent",
    model_client=model,
    system_message="""당신은 마케팅, 행동 심리학, 카피라이팅 교육을 받은 설득 전문가입니다. 당신의 임무는 이메일의 설득력을 높이는 것입니다. 
    구체적으로는 행동 유도(CTA) 개선, 논리 구조 설계, 그리고 혜택(Benefits)을 강조하는 일을 수행합니다. 또한, 힘이 없고 수동적인 표현은 모두 제거하십시오.
    """,
)

# 합성 agent : 모든 아이디를 받아서 이메일에 넣음
synthesizer_agent = AssistantAgent(
    "SynthesizerAgent",
    model_client=model,
    system_message="""당신은 고급 이메일 작성 전문가입니다. 
    당신의 역할은 이전 에이전트들의 모든 응답과 수정 사항을 검토한 뒤, 최상의 아이디어들을 종합하여 통일되고 세련된 이메일 초안을 작성하는 것입니다. 
    다음 사항에 집중해 주세요: 명확성, 어조, 설득력 개선 사항의 통합; 일관성, 유창함, 그리고 자연스러운 목소리 확보; 전문적이고 효과적이며 가독성이 좋은 버전 생성.
    """,
)

# 최종 결과
critic_agent = AssistantAgent(
    "CriticAgent",
    model_client=model,
    system_message="""당신은 이메일 품질 평가자입니다. 
    당신의 임무는 종합된 이메일에 대한 최종 검토를 수행하고 전문적인 기준을 충족하는지 판단하는 것입니다. 
    다음 사항을 검토하십시오: 명확성과 흐름, 적절하고 전문적인 어조, 효과적인 행동 유도, 그리고 전반적인 일관성. 
    건설적이되 단호하게 평가하십시오. 
    이메일에 중대한 결함(불분명한 메시지, 비전문적인 어조 또는 핵심 요소 누락)이 있는 경우, 한 가지 구체적인 개선 제안을 제공하십시오. 
    이메일이 전문적인 기준을 충족하고 효과적으로 전달된다면, 'The email meets professional standards.'라고 응답한 뒤 다음 줄에 TERMINATE를 적으십시오. 
    완벽하지 않더라도 전문적인 용도로 사용하기에 충분히 훌륭하다면 이메일을 승인해야 합니다.
    """,
)