import asyncio
import streamlit as st
from agents import (
    SQLiteSession,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)
from agents.voice import AudioInput, VoicePipeline
from models import UserAccountContext
from my_agents.triage_agent import triage_agent
from workflow import CustomWorkflow

import wave, io
import numpy as np
import sounddevice as sd

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI()

use_account_context = UserAccountContext(
    customer_id=1,
    name="Funky",
    tier="basic",
)

if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history", "customer-support-memory.db"
    )

session = st.session_state["session"]

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent


def convert_audio(audio_input):
    audio_data = audio_input.getvalue()

    with wave.open(io.BytesIO(audio_data), "rb") as wav_file:
        audio_frames = wav_file.readframes(-1)

    return np.frombuffer(
        audio_frames,
        dtype=np.int16,
    )


async def run_agent(audio_input):
    status_container = st.status("⏳ Processing voice message...")

    with st.chat_message("ai"):
        try:
            # 오디오를 Numpy 배열로 변환
            audio_array = convert_audio(audio_input)
            audio = AudioInput(buffer=audio_array)
            # custom workflow 생성
            workflow = CustomWorkflow(context=use_account_context)
            # pipeline 생성
            pipeline = VoicePipeline(workflow=workflow)

            status_container.update(label="Running workflw", state="running")

            result = await pipeline.run(audio)

            player = sd.OutputStream(
                samplerate=24000,
                channels=1,
                dtype=np.int16,
            )
            player.start()

            status_container.update(state="complete")

            async for event in result.stream():
                if event.type == "voice_stream_event_audio":
                    player.write(event.data)

        except InputGuardrailTripwireTriggered:
            st.write("죄송합니다. 사용자의 요청이 주제에서 벗어났습니다.")

        except OutputGuardrailTripwireTriggered:
            st.write("죄송합니다. 응답이 부적절한 내용을 포함하고 있습니다.")


audio_input = st.audio_input(
    "Record your message",
)

if audio_input:
    with st.chat_message("human"):
        st.audio(audio_input)
    asyncio.run(run_agent(audio_input))


with st.sidebar:
    reset = st.button("Reset memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))
