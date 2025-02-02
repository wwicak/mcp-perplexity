from os import getenv
from textwrap import dedent
import json

import httpx
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

PERPLEXITY_API_KEY = getenv("PERPLEXITY_API_KEY")
PERPLEXITY_MODEL = getenv("PERPLEXITY_MODEL")
PERPLEXITY_API_BASE_URL = "https://api.perplexity.ai"


server = Server("mcp-server-perplexity")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="ask_perplexity",
            description=dedent(
                """
                Provides expert programming assistance through Perplexity.
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
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    context = server.request_context
    progress_token = context.meta.progressToken if context.meta else None
    
    if name != "ask_perplexity":
        raise ValueError(f"Unknown tool: {name}")

    system_prompt = dedent("""
        You are an expert assistant providing accurate answers using real-time web searches. 
        Your responses must:
        1. Be based on the most relevant web sources
        2. Include source citations for all factual claims
        3. If no relevant results are found, suggest 2-3 alternative search queries that might better uncover the needed information
        4. Prioritize technical accuracy, especially for programming-related questions
    """).strip()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PERPLEXITY_API_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": PERPLEXITY_MODEL,
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
            usage = {}  # Initialize usage dict
            
            async for chunk in response.aiter_text():
                for line in chunk.split('\n'):
                    line = line.strip()
                    if line.startswith("data: "):
                        try:
                            data = json.loads(line[6:])
                            # Collect usage if present
                            if "usage" in data:
                                usage.update(data["usage"])
                            # Collect citations and content
                            if "citations" in data:
                                citations.extend(data["citations"])
                            if data.get("choices"):
                                content = data["choices"][0].get("delta", {}).get("content", "")
                                full_response += content
                        except json.JSONDecodeError:
                            continue

            # Format citations with numbered list starting from 1
            unique_citations = list(dict.fromkeys(citations))  # Remove duplicates while preserving order
            citation_list = "\n".join(f"{i}. {url}" for i, url in enumerate(unique_citations, start=1))

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
                    progress=2000,
                    total=2000,
                    message="Complete"
                )

            return [
                types.TextContent(
                    type="text", 
                    text=response_text
                )
            ]

    except httpx.HTTPError as e:
        raise RuntimeError(f"API error: {str(e)}")


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
                        notification_options=NotificationOptions(tools_changed=True),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        print(f"Server error: {str(e)}", flush=True)
        raise
    print("Server shutdown", flush=True)
