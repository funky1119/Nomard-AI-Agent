import asyncio
import base64

import streamlit as st
from agents import (
    Agent,
    FileSearchTool,
    ImageGenerationTool,
    Runner,
    SQLiteSession,
    CodeInterpreterTool,
    HostedMCPTool,
)
from agents.mcp.server import MCPServerStdio
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

VECTOR_STORE_ID = "vs_698ecb6fc2708191b5aa02f0ce497af6"

if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history", "chat-gpt-clone-memory.db"
    )

session = st.session_state["session"]

if "_orig_get_items" not in st.session_state:
    st.session_state["_orig_get_items"] = session.get_items


def _strip_action(obj):
    if isinstance(obj, dict):
        obj.pop("action", None)
        for k, v in list(obj.items()):
            obj[k] = _strip_action(v)
        return obj
    if isinstance(obj, list):
        return [_strip_action(x) for x in obj]
    return obj


async def safe_get_items(*args, **kwargs):
    items = await st.session_state["_orig_get_items"](*args, **kwargs)
    return _strip_action(items)


if not st.session_state.get("_session_get_items_patched", False):
    session.get_items = safe_get_items
    st.session_state["_session_get_items_patched"] = True


async def paint_history():
    messages = await safe_get_items()

    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    content = message["content"]
                    if isinstance(content, str):
                        st.write(content)
                    elif isinstance(content, list):
                        for part in content:
                            if "image_url" in part:
                                st.image(part["image_url"])
                else:
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"].replace("$", r"\$"))
        if "type" in message:
            message_type = message["type"]
            if message_type == "web_search_call":
                with st.chat_message("ai"):
                    st.write("🔎 Searched the web...")

            elif message_type == "file_search_call":
                with st.chat_message("ai"):
                    st.write("🗂️ Searched files...")

            elif message_type == "image_generation_call":
                image = base64.b64decode(message["result"])
                with st.chat_message("ai"):
                    st.image(image)

            elif message_type == "code_interpreter_call":
                with st.chat_message("ai"):
                    st.code(message["code"])

            elif message_type == "mcp_list_tools":
                with st.chat_message("ai"):
                    st.write(f"List {message['server_label']}'s tools")

            elif message_type == "mcp_call":
                with st.chat_message("ai"):
                    st.write(
                        f"Called {message['server_label']}'s {message['name']} with args {message['arguments']}"
                    )


asyncio.run(paint_history())


def update_status(status_container, event):

    status_message = {
        "response.web_search_call.completed": ("✅ Web search completed.", "complete"),
        "response.web_search_call.in_progress": (
            "🔎 Starting web search...",
            "running",
        ),
        "response.web_search_call.searching": (
            "🔎 Web search in progress...",
            "running",
        ),
        "response.file_search_call.completed": (
            "✅ File search completed.",
            "complete",
        ),
        "response.file_search_call.in_progress": (
            "🗂️ Starting file search...",
            "running",
        ),
        "response.file_search_call.searching": (
            "🗂️ File search in progress...",
            "running",
        ),
        "response.image_generation_call.generating": ("🎨 Drawing image...", "running"),
        "response.image_generation_call.in_progress": (
            "🎨 Drawing image...",
            "running",
        ),
        "response.code_interpreter_call_code.done": ("🤖 Ran code.", "complete"),
        "response.code_interpreter_call.completed": ("🤖 Ran code.", "complete"),
        "response.code_interpreter_call.in_progress": (
            "🤖 Running code...",
            "complete",
        ),
        "response.code_interpreter_call.interpreting": (
            "🤖 Running code...",
            "complete",
        ),
        "response.mcp_call.completed": (
            "⚒️ Called MCP tool",
            "complete",
        ),
        "response.mcp_call.failed": (
            "⚒️ Error calling MCP tool",
            "complete",
        ),
        "response.mcp_call.in_progress": (
            "⚒️ Calling MCP tool...",
            "running",
        ),
        "response.mcp_list_tools.completed": (
            "⚒️ Listed MCP tools",
            "complete",
        ),
        "response.mcp_list_tools.failed": (
            "⚒️ Error listing MCP tools",
            "complete",
        ),
        "response.mcp_list_tools.in_progress": (
            "⚒️ Listing MCP tools",
            "running",
        ),
        "response.completed": ("✅", "complete"),
    }

    if event in status_message:
        label, state = status_message[event]
        status_container.update(label=label, state=state)


async def run_agent(message):
    yfinance_server = MCPServerStdio(
        params={
            "command": "uvx",
            "args": ["mcp-yahoo-finance"],
        },
        cache_tools_list=True,
        client_session_timeout_seconds=30,
        max_retry_attempts=2,
    )

    timezone_server = MCPServerStdio(
        params={
            "command": "uvx",
            "args": ["mcp-server-time", "--local-timezone=Asia/Seoul"],
        },
        cache_tools_list=True,
        client_session_timeout_seconds=30,
        max_retry_attempts=2,
    )

    async with yfinance_server, timezone_server:
        agent = Agent(
            mcp_servers=[
                yfinance_server,
                timezone_server,
            ],
            name="ChatGPT Clone",
            model="gpt-4o-mini",
            instructions="""
            You are a helpful assistant.

            You have access to the following tolls:
            - Web Search Tool: Use this when the user asks a questions that isn't in your training data. Use this tool when the users asks about current or future events, when you think you don't know the answer, try searching for it in the web first.
            - File Search Tool: Use this tool when the user asks a question about facts related to themselves. Or when they ask questions about specific files.
            """,
            tools=[
                FileSearchTool(
                    vector_store_ids=[VECTOR_STORE_ID],
                    max_num_results=3,
                ),
                ImageGenerationTool(
                    tool_config={
                        "type": "image_generation",
                        "quality": "low",
                        "output_format": "jpeg",
                        "partial_images": 1,
                    }
                ),
                CodeInterpreterTool(
                    tool_config={
                        "type": "code_interpreter",
                        "container": {"type": "auto"},
                    }
                ),
                HostedMCPTool(
                    tool_config={
                        "server_url": "https://mcp.context7.com/mcp",
                        "type": "mcp",
                        "server_label": "Context7",
                        "server_description": "Use this tool get the doc from software projects.",
                        "require_approval": "never",
                    }
                ),
            ],
        )

        with st.chat_message("ai"):
            status_container = st.status("⏳", expanded=False)
            code_placeholder = st.empty()
            image_placeholder = st.empty()
            text_placeholder = st.empty()
            response = ""

            st.session_state["code_placeholder"] = code_placeholder
            st.session_state["image_placeholder"] = image_placeholder
            st.session_state["text_placeholder"] = text_placeholder

            stream = Runner.run_streamed(agent, message, session=session)

            async for event in stream.stream_events():
                if event.type == "raw_response_event":
                    update_status(status_container, event.data.type)

                    if event.data.type == "response.output_text.delta":
                        response += event.data.delta
                        text_placeholder.write(response)

                    elif (
                        event.data.type
                        == "response.image_generation_call.partial_image"
                    ):
                        image = base64.b64decode(event.data.partial_image_b64)
                        image_placeholder.image(image)


prompt = st.chat_input(
    "Write a message for your assistant",
    accept_file=True,
    file_type=["txt", "jpg", "png", "jpeg"],
)

if prompt:
    if "code_placeholder" in st.session_state:
        st.session_state["code_placeholder"].empty()
    if "image_placeholder" in st.session_state:
        st.session_state["image_placeholder"].empty()
    if "text_placeholder" in st.session_state:
        st.session_state["text_placeholder"].empty()

    for file in prompt.files:
        if file.type.startswith("text/"):
            with st.chat_message("ai"):
                with st.status("⏳ Uploading file...") as status:
                    uploaded_file = client.files.create(
                        file=(file.name, file.getvalue()), purpose="user_data"
                    )
                    status.update(label="⏳ Attaching file...")
                    client.vector_stores.files.create(
                        vector_store_id=VECTOR_STORE_ID,
                        file_id=uploaded_file.id,
                    )
                    status.update(label="✅ File uploaded.", state="complete")
        elif file.type.startswith("image/"):
            with st.status("⏳ Uploading image...") as status:
                file_byte = file.getvalue()
                base64_data = base64.b64encode(file_byte).decode("utf-8")
                data_uri = f"data:{file.type};base64,{base64_data}"
                asyncio.run(
                    session.add_items(
                        [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "input_image",
                                        "detail": "auto",
                                        "image_url": data_uri,
                                    }
                                ],
                            }
                        ]
                    )
                )
                status.update(label="✅ Image uploaded.", state="complete")
            with st.chat_message("human"):
                st.image(data_uri)

    if prompt.text:
        with st.chat_message("human"):
            st.write(prompt.text)
        asyncio.run(run_agent(prompt.text))


with st.sidebar:
    reset = st.button("Reset memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(safe_get_items()))
