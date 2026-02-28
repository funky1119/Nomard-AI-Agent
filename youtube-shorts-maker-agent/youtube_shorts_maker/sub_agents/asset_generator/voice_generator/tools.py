from google.genai import types
from openai import OpenAI
from google.adk.tools.tool_context import ToolContext
from typing import List, Dict, Any

client = OpenAI()


async def generate_narrations(
    tool_context: ToolContext, voice: str, voice_instructions: List[Dict[str, Any]]
):
    """
    OpenAI TTS API를 사용하여 각 장면의 내레이션 오디오를 생성합니다.

    Args:
        tool_context: 아티팩트에 접근하고 파일을 저장하기 위한 도구 컨텍스트
        voice: TTS에 사용할 선택된 음성 (alloy, echo, fable, onyx, nova, shimmer)
        voice_instructions: 각 장면의 내레이션 지시사항이 담긴 딕셔너리 목록 

    Returns:
        생성된 모든 오디오 파일 정보
    """

    existing_artifacts = await tool_context.list_artifacts()

    generated_narrations = []

    for instruction in voice_instructions:
        text_input = instruction.get("input")
        instructions = instruction.get("instructions")
        scene_id = instruction.get("scene_id")
        filename = f"scene_{scene_id}_narration.mp3"

        if filename in existing_artifacts:
            generated_narrations.append(
                {
                    "scene_id": scene_id,
                    "filename": filename,
                    "input": text_input,
                    "instructions": instructions[:50],
                }
            )
            continue

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text_input,
            instructions=instructions,
        ) as response:
            audio_data = response.read()

        artifact = types.Part(
            inline_data=types.Blob(mime_type="audio/mpeg", data=audio_data)
        )

        await tool_context.save_artifact(filename=filename, artifact=artifact)

        generated_narrations.append(
            {
                "scene_id": scene_id,
                "filename": filename,
                "input": text_input,
                "instructions": instructions[:50],
            }
        )

    return {
        "success": True,
        "narrations": generated_narrations,
        "total_narrations": len(generated_narrations),
    }
