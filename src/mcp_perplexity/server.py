import os
from textwrap import dedent
import json
from collections import deque

import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from haikunator import Haikunator
import sqlite3
from datetime import datetime
import uuid

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_MODEL = os.getenv("PERPLEXITY_MODEL")
PERPLEXITY_MODEL_ASK = os.getenv("PERPLEXITY_MODEL_ASK")
PERPLEXITY_MODEL_CHAT = os.getenv("PERPLEXITY_MODEL_CHAT")
PERPLEXITY_API_BASE_URL = "https://api.perplexity.ai"

haikunator = Haikunator()
DB_PATH = os.getenv("DB_PATH", "chats.db")
SYSTEM_PROMPT = """You are an expert assistant providing accurate answers to technical questions. 
Your responses must:
1. Be based on the most relevant web sources
2. Include source citations for all factual claims
3. If no relevant results are found, suggest 2-3 alternative search queries that might better uncover the needed information
4. Prioritize technical accuracy, especially for programming-related questions"""

server = Server("mcp-server-perplexity")


def init_db():
    try:
        # Create parent directories if needed
        db_dir = os.path.dirname(DB_PATH)
        if db_dir:  # Only create directories if path contains them
            os.makedirs(db_dir, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create tables with enhanced error handling
        c.execute('''CREATE TABLE IF NOT EXISTS chats
                     (id TEXT PRIMARY KEY,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      title TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS messages
                     (id TEXT PRIMARY KEY,
                      chat_id TEXT,
                      role TEXT,
                      content TEXT,
                      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY(chat_id) REFERENCES chats(id))''')

        # Verify table creation
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('chats', 'messages')")
        existing_tables = {row[0] for row in c.fetchall()}
        if 'chats' not in existing_tables or 'messages' not in existing_tables:
            raise RuntimeError("Failed to create database tables")

        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection error: {str(e)}")
    except Exception as e:
        raise RuntimeError(
            f"Failed to initialize database at '{DB_PATH}': {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()


# Initialize database on startup
init_db()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="ask_perplexity",
            description=dedent(
                """
                Provides expert programming assistance through Perplexity.
                This tool only has access to the context you have provided. It cannot read any file unless you provide it with the file content.
                Focuses on coding solutions, error debugging, and technical explanations.
                Returns responses with source citations and alternative suggestions.
                """
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Technical question or problem to solve"
                    }
                },
                "required": ["query"]
            },
        ),
        types.Tool(
            name="chat_perplexity",
            description=dedent("""
                Maintains ongoing conversations with Perplexity AI.
                Creates new chats or continues existing ones with full history context.
                This tool only has access to the context you have provided. It cannot read any file unless you provide it with the file content.
                Returns chat ID for future continuation.
                """),
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "New message to add to the conversation"
                    },
                    "chat_id": {
                        "type": "string",
                        "description": "Existing chat ID to continue (optional)"
                    },
                    "title": {
                        "type": "string",
                        "description": "Optional title for new chat"
                    }
                },
                "required": ["message"]
            },
        )
    ]


def generate_chat_id():
    return haikunator.haikunate(token_length=2, delimiter='-').lower()


def store_message(chat_id, role, content, title=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create chat if it doesn't exist
    c.execute("INSERT OR IGNORE INTO chats (id, title) VALUES (?, ?)",
              (chat_id, title))

    # Store message
    c.execute("INSERT INTO messages (id, chat_id, role, content) VALUES (?, ?, ?, ?)",
              (str(uuid.uuid4()), chat_id, role, content))

    conn.commit()
    conn.close()


def get_chat_history(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''SELECT role, content FROM messages 
                 WHERE chat_id = ? 
                 ORDER BY timestamp''', (chat_id,))
    history = [{"role": row[0], "content": row[1]} for row in c.fetchall()]
    conn.close()
    return history


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    context = server.request_context
    progress_token = context.meta.progressToken if context.meta else None

    if name == "ask_perplexity":
        system_prompt = dedent(SYSTEM_PROMPT).strip()

        try:
            # Initialize progress tracking with dynamic estimation
            initial_estimate = 1000
            progress_counter = 0
            total_estimate = initial_estimate
            chunk_sizes = deque(maxlen=10)  # Store last 10 chunk sizes
            chunk_count = 0

            if progress_token:
                await context.session.send_progress_notification(
                    progress_token=progress_token,
                    progress=0,
                    total=initial_estimate,
                )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{PERPLEXITY_API_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": PERPLEXITY_MODEL_ASK or PERPLEXITY_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": arguments["query"]}
                        ],
                        "stream": True
                    },
                    timeout=30.0,
                )
                response.raise_for_status()

                citations = []
                full_response = ""
                usage = {}

                async for chunk in response.aiter_text():
                    for line in chunk.split('\n'):
                        line = line.strip()
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                if "usage" in data:
                                    usage.update(data["usage"])
                                if "citations" in data:
                                    citations.extend(data["citations"])
                                if data.get("choices"):
                                    content = data["choices"][0].get(
                                        "delta", {}).get("content", "")
                                    full_response += content

                                    # Update progress with dynamic estimation
                                    tokens_in_chunk = len(content.split())
                                    progress_counter += tokens_in_chunk
                                    chunk_count += 1
                                    chunk_sizes.append(tokens_in_chunk)

                                    # Update total estimate every 5 chunks
                                    if chunk_count % 5 == 0 and chunk_sizes:
                                        avg_chunk_size = sum(
                                            chunk_sizes) / len(chunk_sizes)
                                        total_estimate = max(initial_estimate,
                                                             int(progress_counter + avg_chunk_size * 10))

                                    if progress_token:
                                        await context.session.send_progress_notification(
                                            progress_token=progress_token,
                                            progress=progress_counter,
                                            total=total_estimate,
                                        )
                            except json.JSONDecodeError:
                                continue

                # Format citations with numbered list starting from 1
                unique_citations = list(dict.fromkeys(citations))
                citation_list = "\n".join(
                    f"{i}. {url}" for i, url in enumerate(unique_citations, start=1))

                response_text = (
                    f"{full_response}\n\n"
                    f"Sources:\n{citation_list}\n\n"
                    f"API Usage:\n"
                    f"- Prompt tokens: {usage.get('prompt_tokens', 'N/A')}\n"
                    f"- Completion tokens: {usage.get('completion_tokens', 'N/A')}\n"
                    f"- Total tokens: {usage.get('total_tokens', 'N/A')}"
                )

                if progress_token:
                    await context.session.send_progress_notification(
                        progress_token=progress_token,
                        progress=progress_counter,
                        total=progress_counter,  # Set final total to actual tokens received
                    )

                return [
                    types.TextContent(
                        type="text",
                        text=response_text
                    )
                ]

        except httpx.HTTPError as e:
            if progress_token:
                await context.session.send_progress_notification(
                    progress_token=progress_token,
                    progress=progress_counter if 'progress_counter' in locals() else 0,
                    total=progress_counter if 'progress_counter' in locals() else 0,
                )
            raise RuntimeError(f"API error: {str(e)}")

    elif name == "chat_perplexity":
        chat_id = arguments.get("chat_id") or generate_chat_id()
        user_message = arguments["message"]
        title = arguments.get("title")

        # Store user message
        store_message(chat_id, "user", user_message, title)

        # Get full chat history
        chat_history = get_chat_history(chat_id)

        system_prompt = dedent(SYSTEM_PROMPT).strip()

        # Initialize progress tracking with dynamic estimation
        initial_estimate = 1000
        progress_counter = 0
        total_estimate = initial_estimate
        chunk_sizes = deque(maxlen=10)  # Store last 10 chunk sizes
        chunk_count = 0

        try:
            if progress_token:
                await context.session.send_progress_notification(
                    progress_token=progress_token,
                    progress=0,
                    total=initial_estimate,
                )

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{PERPLEXITY_API_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": PERPLEXITY_MODEL_CHAT or PERPLEXITY_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            *chat_history,
                        ],
                        "stream": True
                    },
                    timeout=30.0,
                )
                response.raise_for_status()

                citations = []
                full_response = ""
                usage = {}

                async for chunk in response.aiter_text():
                    for line in chunk.split('\n'):
                        line = line.strip()
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                if "usage" in data:
                                    usage.update(data["usage"])
                                if "citations" in data:
                                    citations.extend(data["citations"])
                                if data.get("choices"):
                                    content = data["choices"][0].get(
                                        "delta", {}).get("content", "")
                                    full_response += content

                                    # Update progress with dynamic estimation
                                    tokens_in_chunk = len(content.split())
                                    progress_counter += tokens_in_chunk
                                    chunk_count += 1
                                    chunk_sizes.append(tokens_in_chunk)

                                    # Update total estimate every 5 chunks
                                    if chunk_count % 5 == 0 and chunk_sizes:
                                        avg_chunk_size = sum(
                                            chunk_sizes) / len(chunk_sizes)
                                        total_estimate = max(initial_estimate,
                                                             int(progress_counter + avg_chunk_size * 10))

                                    if progress_token:
                                        await context.session.send_progress_notification(
                                            progress_token=progress_token,
                                            progress=progress_counter,
                                            total=total_estimate,
                                        )
                            except json.JSONDecodeError:
                                continue

                # Format citations with numbered list starting from 1
                unique_citations = list(dict.fromkeys(citations))
                citation_list = "\n".join(
                    f"{i}. {url}" for i, url in enumerate(unique_citations, start=1))

                # Store assistant response
                store_message(chat_id, "assistant", full_response)

                # Format chat history
                history_text = "\nChat History:\n"
                for msg in chat_history:
                    role = "You" if msg["role"] == "user" else "Assistant"
                    history_text += f"\n{role}: {msg['content']}\n"

                response_text = (
                    f"Chat ID: {chat_id}\n"
                    f"{history_text}\n"
                    f"Current Response:\n{full_response}\n\n"
                    f"Sources:\n{citation_list}"
                )

                if progress_token:
                    await context.session.send_progress_notification(
                        progress_token=progress_token,
                        progress=progress_counter,
                        total=progress_counter,  # Set final total to actual tokens received
                    )

                return [
                    types.TextContent(
                        type="text",
                        text=response_text
                    )
                ]

        except httpx.HTTPError as e:
            if progress_token:
                await context.session.send_progress_notification(
                    progress_token=progress_token,
                    progress=progress_counter if 'progress_counter' in locals() else 0,
                    total=progress_counter if 'progress_counter' in locals() else 0,
                )
            raise RuntimeError(f"API error: {str(e)}")

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():

    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-server-perplexity",
                    server_version="0.1.2",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(
                            tools_changed=True),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        print(f"Server error: {str(e)}", flush=True)
        raise
    print("Server shutdown", flush=True)
