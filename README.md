# Perplexity MCP Server

MCP Server for the Perplexity API.

[![smithery badge](https://smithery.ai/badge/@daniel-lxs/mcp-perplexity)](https://smithery.ai/server/@daniel-lxs/mcp-perplexity)

[![PyPI Publish](https://github.com/daniel-lxs/mcp-perplexity/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/daniel-lxs/mcp-perplexity/actions/workflows/pypi-publish.yml)

<a href="https://glama.ai/mcp/servers/0nggjl0ohi">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/0nggjl0ohi/badge" />
</a>

## Components

### Tools

- **ask_perplexity**: Request expert programming assistance through Perplexity. Focuses on coding solutions, error debugging, and technical explanations. Returns responses with source citations and alternative suggestions.
- **chat_perplexity**: Maintains ongoing conversations with Perplexity AI. Creates new chats or continues existing ones with full history context. Returns chat ID for future continuation.

## Key Features

- **Model Configuration via Environment Variable:**  Allows you to specify the Perplexity model using the `PERPLEXITY_MODEL` environment variable for flexible model selection.  You can also specify `PERPLEXITY_MODEL_ASK` and `PERPLEXITY_MODEL_CHAT` to use different models for the `ask_perplexity` and `chat_perplexity` tools, respectively.  These will override `PERPLEXITY_MODEL`. You can check which models are available on the [Perplexity](https://docs.perplexity.ai/guides/model-cards) documentation.
- **Persistent Chat History:** The `chat_perplexity` tool maintains ongoing conversations with Perplexity AI. Creates new chats or continues existing ones with full history context. Returns chat ID for future continuation.
- **Streaming Responses with Progress Reporting:** Uses progress reporting to prevent timeouts on slow responses.

## Quickstart

### Installation

#### Installing via Smithery

To install Perplexity MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@daniel-lxs/mcp-perplexity):

```bash
npx -y @smithery/cli install @daniel-lxs/mcp-perplexity --client claude
```

#### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [uvx](https://docs.astral.sh/uv/getting-started/installation/) (recommended)

**How to install uvx on Windows:**
Open PowerShell as Administrator and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Windows Installation Notes:**
- Ensure Python 3.10+ is installed and added to PATH
- The installation script will handle uvx setup
- Your MCP client will manage package installation via the provided configuration

#### Configure your MCP Client

To use this MCP server, you need to configure your MCP client to connect to it. The configuration method will vary depending on your specific client.

Below is an example configuration in JSON format:

```json
"mcpServers": {
  "Perplexity": {
    "command": "uvx",
    "args": [
      "mcp-perplexity"
    ],
    "env": {
      "PERPLEXITY_API_KEY": "your-perplexity-api-key",
      "PERPLEXITY_MODEL": "sonar-pro"
    }
  }
}
```

**Important notes:**
- Replace `"your-perplexity-api-key"` with your actual Perplexity API key.
- You can also set `PERPLEXITY_MODEL_ASK` and `PERPLEXITY_MODEL_CHAT` to override `PERPLEXITY_MODEL` for the individual tools.
- Consult your MCP client's documentation for details on where to place this configuration and any client-specific settings.
- Use the [mcp-starter](https://github.com/daniel-lxs/mcp-starter) script to easily add this MCP server to Cursor IDE.
