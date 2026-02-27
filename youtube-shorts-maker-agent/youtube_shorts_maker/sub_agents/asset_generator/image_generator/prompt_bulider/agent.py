from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prompt import PROMPT_BUILDER_DESCRIPTION, PROMPT_BUILDER_PROMPT
from pydantic import BaseModel, Field, ConfigDict
from typing import List

MODEL = LiteLlm(model="openai/gpt-4o")

class OptimizedPrompt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scene_id: int = Field(description="원본 콘텐츠 계획의 장면 ID")
    enhanced_prompt: str = Field(
        description="세로형 YouTube Shorts를 위한 기술 사양 및 텍스트 오버레이 지침이 포함된 상세 프롬프트"
    )


class PromptBuilderOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    optimized_prompts: List[OptimizedPrompt] = Field(description="세로형 YouTube Shorts를 위한 최적화된 이미지 생성 프롬프트 배열")
    

prompt_bulider_agent = Agent(
    name="PromptBuilderAgent",
    description=PROMPT_BUILDER_DESCRIPTION,
    instruction=PROMPT_BUILDER_PROMPT,
    model= MODEL,
    output_schema=PromptBuilderOutput,
    output_key="prompt_builder_oupt",
    
)
