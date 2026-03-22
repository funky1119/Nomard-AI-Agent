from langgraph.graph import END, START, StateGraph
from langgraph.types import Send, interrupt, Command
from typing import TypedDict
import subprocess
from openai import OpenAI
import textwrap
from langchain.chat_models import init_chat_model
from typing_extensions import Annotated
import operator
import base64

llm = init_chat_model("openai:gpt-4o-mini")

class State(TypedDict):
    video_file: str
    audio_file: str
    transcription: str
    summaries: Annotated[list[str], operator.add]
    thumbnail_prompts: Annotated[list[str], operator.add]
    thumbnail_sketches: Annotated[list[str], operator.add]
    final_summary: str
    user_feedback: str
    chosen_prompt: str

def extract_audio(state: State):
    output_file = state["video_file"].replace("mp4", "mp3")
    command = [
        "ffmpeg",
        "-i",
        state["video_file"],
        "-filter:a",
        "atempo=2.0",
        "-y",
        output_file
    ]
    subprocess.run(command)
    return  {
        "audio_file": output_file
    }

def transcribe_audio(state: State):
    client = OpenAI()
    with open(state["audio_file"], "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file,
            prompt="프랑스 대혁명에 관련된 내용이야"
        )
        return {
            "transcription": transcription
        }

def dispatch_summarizers(state: State):
    transcription = state["transcription"]
    chunks = []
    for i, chunk in enumerate(textwrap.wrap(transcription, 500)):
        chunks.append({"id": i+1, "chunk": chunk})
    
    return [Send("summarize_chunk", chunk) for chunk in chunks]

def summarize_chunk(chunk):
    chunk_id = chunk["id"]
    chunk = chunk["chunk"]

    response = llm.invoke(
        f"""
        다음의 텍스트를 요약하세요.

        Text: {chunk}
        """
    )
    summary = f"[Chunk {chunk_id}] {response.content}"
    return  {
        "summaries": [summary],
    }

def mega_summary(state: State):
    all_summaries = "\n".join(state["summaries"])

    prompt = f"""
    너는 한 영상에서 나온 텍스트의 여러 청크들로 만든 요약본을 받을 거야
    모든 핵심 포인트를 결합한 종합 요약본을 작성해 줘

    개별 요약본들: 
    
    {all_summaries}
    """

    response = llm.invoke(prompt)

    return {
        "final_summary": response.content
    }
    
def dispatch_artists(state: State):
    return  [
        Send(
            "generate_thumbnails", 
            {
                "id": i, 
                "summary": state["final_summary"]
            }
        ) for i in [1,2,3,4,5]
    ]

def generate_thumbnails(args):
    concept_id = args["id"]
    summary = args["summary"]
    
    prompt = f""",
    이 영상 요약을 바탕으로 유튜브 썸네일용 상세 비주얼 프롬프트를 만들어줘.

    시청자의 클릭을 유도할 수 있는 썸네일 이미지를 생성하기 위한 상세 프롬프트를 작성해줘. 다음 내용을 포함해:
    - 주요 시각 요소
    - 색상 구성
    - 텍스트 오버레이 제안
    - 전체적인 구도

    요약: {summary}
    """

    response = llm.invoke(prompt)

    thumbnail_prompt = response.content

    client = OpenAI()

    result = client.images.generate(
        model="gpt-image-1",
        prompt=thumbnail_prompt,
        quality="low",
        moderation="low",
        size="auto",
    )

    image_bytes = base64.b64decode(result.data[0].b64_json)

    filename = f"thumbnail_{concept_id}.jpg"

    with open(filename, "wb") as file:
        file.write(image_bytes)

    return {
        "thumbnail_prompts": [thumbnail_prompt],
        "thumbnail_sketches": [filename]
    }

def human_feedback(state: State):
    answer = interrupt({
        "chosen_thumbnail": "어떤 썸네일이 가장 마음에 드셨나요?",
        "feedback": "최종 썸네일에 원하는 피드백이나 변경사항을 제공해주세요.",
    })
    user_feedback = answer["user_feedback"]
    chosen_prompt= answer["chosen_prompt"]

    return {
        "user_feedback": user_feedback,
        "chosen_prompt": state["thumbnail_prompts"][chosen_prompt-1]
    }

def generate_hd_thumbnail(state: State):
    chosen_prompt = state["chosen_prompt"]
    user_feedback = state["user_feedback"]

    prompt = f"""
    당신은 전문 유튜브 썸네일 디자이너입니다. 아래의 원본 썸네일 프롬프트를 바탕으로, 사용자가 남긴 구체적인 피드백을 반영한 향상된 버전을 만들어주세요.

    원본 프롬프트:
    {chosen_prompt}

    반영할 사용자 피드백:
    {user_feedback}

    다음 조건을 만족하는 향상된 프롬프트를 작성해주세요:

    1. 원본 프롬프트의 핵심 콘셉트는 유지할 것
    2. 사용자의 피드백 요청을 구체적으로 반영하고 구현할 것
    3. 전문적인 유튜브 썸네일 제작 기준을 추가로 반영할 것
        - 높은 대비와 강한 시각 요소
        - 시선을 끄는 명확한 초점 요소
        - 전문적인 조명과 구도
        - 텍스트 배치의 최적화 및 가독성 확보, 그리고 이미지 가장자리로부터 충분한 여백 확보
        - 눈에 잘 띄고 주목도를 높이는 색상 사용
        - 작은 썸네일 크기에서도 잘 보이는 요소 구성
        - 중요: 모든 텍스트는 이미지 경계선과 충분한 여백/패딩을 반드시 확보할 것
    """

    response = llm.invoke(prompt)

    final_thumbnail_prompt = response.content

    client = OpenAI()

    result = client.images.generate(
        model="gpt-image-1",
        prompt=final_thumbnail_prompt,
        quality="high",
        moderation="low",
        size="auto",
    )

    image_bytes = base64.b64decode(result.data[0].b64_json)

    with open("thumbnail_final.jpg", "wb") as file:
        file.write(image_bytes)


graph_builder = StateGraph(State)

graph_builder.add_node("extract_audio", extract_audio)
graph_builder.add_node("transcribe_audio", transcribe_audio)
graph_builder.add_node("summarize_chunk", summarize_chunk)
graph_builder.add_node("mega_summary", mega_summary)
graph_builder.add_node("generate_thumbnails", generate_thumbnails)
graph_builder.add_node("human_feedback", human_feedback)
graph_builder.add_node("generate_hd_thumbnail", generate_hd_thumbnail)


graph_builder.add_edge(START, "extract_audio")
graph_builder.add_edge("extract_audio", "transcribe_audio")
graph_builder.add_conditional_edges("transcribe_audio", dispatch_summarizers, ["summarize_chunk"])
graph_builder.add_edge("summarize_chunk", "mega_summary")
graph_builder.add_conditional_edges("mega_summary", dispatch_artists, ["generate_thumbnails"])
graph_builder.add_edge("generate_thumbnails", "human_feedback")
graph_builder.add_edge("human_feedback", "generate_hd_thumbnail")
graph_builder.add_edge("generate_hd_thumbnail", END)


graph = graph_builder.compile(name="mr_thumbs")
