from langchain_core.tools import tool
from typing import Literal, List
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field


class Question(BaseModel):

    question: str = Field(description="퀴즈 문제 문장")
    options: List[str] = Field(
        description="A, B, C, D로 구분된 객관식 선택지 4개"
    )
    correct_answer: str = Field(
        description="정답 선택지('options' 중 하나와 정확히 일치해야 함)"
    )
    explanation: str = Field(
        description="왜 이 답이 정답이고 나머지가 오답인지 설명하는 해설"
    )


class Quiz(BaseModel):
    topic: str = Field(description="평가 대상이 되는 핵심 주제")
    questions: List[Question] = Field(description="퀴즈 문제 목록")


@tool
def generate_quiz(
    research_text: str,
    topic: str,
    difficulty: Literal[
        "easy",
        "medium",
        "hard",
    ],
    num_questions: int,
):
    """
    조사 정보를 바탕으로 객관식 구조화 퀴즈를 생성합니다.

    매개변수:
        research_text: 주제에 관한 조사 정보입니다. 예를 들면 다음이 가능합니다:
                      - 웹 검색에서 얻은 원문 텍스트
                      - 조사 결과 요약
                      - 해당 주제와 관련된 기타 정보
                      - 비어 있으면 일반 지식을 바탕으로 문제를 생성합니다

        topic: 퀴즈의 핵심 주제입니다
               (예: "파이썬 프로그래밍", "제2차 세계대전", "광합성")

        difficulty: 난이도입니다.
                   - "easy": 기본 개념, 정의, 단순 사실
                   - "medium": 개념 적용, 아이디어 간 연결
                   - "hard": 복합 분석, 종합, 심화 이해

        num_questions: 생성할 문제 수입니다(1~30)
                      일반적인 값: 3~5(short), 6~10(medium), 11~15(long)

    반환값:
        다음 정보를 포함한 Quiz 객체를 반환합니다:
        - question: 문제 문장
        - options: 객관식 선택지 4개
        - correct_answer: 정답 선택지
        - explanation: 정답에 대한 자세한 해설

    예시:
        research_info = "기계 학습은 알고리즘에 초점을 맞춘 AI의 하위 분야입니다..."
        quiz = generate_quiz(research_info, "기계 학습", "medium", 5)
    """
    model = init_chat_model("openai:gpt-4o")
    structured_model = model.with_structured_output(Quiz)

    prompt = f"""
    다음 조사 정보를 바탕으로 {topic}에 대한 {difficulty} 난이도 퀴즈 {num_questions}문항을 만들어 주세요.

    <RESEARCH_INFORMATION>
    {research_text}
    </RESEARCH_INFORMATION>

    RESEARCH_INFORMATION을 최대한 충실히 반영해서 정확한 문제를 생성하세요.
    모든 문제는 선택지 4개를 가져야 하며, 해설은 한국어로 자세히 작성하세요.
    """

    quiz = structured_model.invoke(prompt)

    return quiz
