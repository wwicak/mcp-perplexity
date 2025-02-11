# Perplexity MCP Server

MCP Server for the Perplexity API.

[![smithery badge](https://smithery.ai/badge/@daniel-lxs/mcp-perplexity)](https://smithery.ai/server/@daniel-lxs/mcp-perplexity) [![PyPI Publish](https://github.com/daniel-lxs/mcp-perplexity/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/daniel-lxs/mcp-perplexity/actions/workflows/pypi-publish.yml)



<a href="https://glama.ai/mcp/servers/0nggjl0ohi">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/0nggjl0ohi/badge" />
</a>

## Components

### Tools

- **ask_perplexity**: Request expert programming assistance through Perplexity. Focuses on coding solutions, error debugging, and technical explanations. Returns responses with source citations and alternative suggestions.
- **chat_perplexity**: Maintains ongoing conversations with Perplexity AI. Creates new chats or continues existing ones with full history context. Returns chat ID for future continuation.

## Key Features

- **Model Configuration via Environment Variable:**  Allows you to specify the Perplexity model using the `PERPLEXITY_MODEL` environment variable for flexible model selection.

  You can also specify `PERPLEXITY_MODEL_ASK` and `PERPLEXITY_MODEL_CHAT` to use different models for the `ask_perplexity` and `chat_perplexity` tools, respectively.

  These will override `PERPLEXITY_MODEL`. You can check which models are available on the [Perplexity](https://docs.perplexity.ai/guides/model-cards) documentation.
- **Persistent Chat History:** The `chat_perplexity` tool maintains ongoing conversations with Perplexity AI. Creates new chats or continues existing ones with full history context. Returns chat ID for future continuation.
- **Streaming Responses with Progress Reporting:** Uses progress reporting to prevent timeouts on slow responses.

## Quickstart

### Installation

#### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [uvx](https://docs.astral.sh/uv/getting-started/installation/) (recommended)

<details>
<summary><h3>Installing uvx</h3></summary>

<details>
<summary><h4>Windows Installation</h4></summary>

Open PowerShell as Administrator and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Windows Installation Notes:**
- Ensure Python 3.10+ is installed and added to PATH

</details>

<details>
<summary><h4>Unix Installation (Linux/MacOS)</h4></summary>

Run the following command in your terminal:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Unix Installation Notes:**
- The script will install uvx to ~/.cargo/bin by default
- You may need to restart your terminal session after installation

</details>

</details>

#### Configure your MCP Client

To use this MCP server, you need to configure your MCP client to connect to it. The configuration method will vary depending on your specific client.

Below is an example configuration in JSON format:

```json
"mcpServers": {
  "mcp-perplexity": {
    "command": "uvx",
    "args": [
      "mcp-perplexity"
    ],
    "env": {
      "PERPLEXITY_API_KEY": "your-perplexity-api-key",
      "PERPLEXITY_MODEL": "sonar-pro",
      "PERPLEXITY_MODEL_ASK": "sonar-pro",
      "PERPLEXITY_MODEL_CHAT": "sonar-reasoning-pro",
      "DB_PATH": "path/to/custom.db"
    }
  }
}
```
**Important notes:**
- Replace `"your-perplexity-api-key"` with your actual Perplexity API key
- Environment variables configuration:
  - `PERPLEXITY_MODEL`: Default model for both tools
  - `PERPLEXITY_MODEL_ASK`: Overrides default model for `ask_perplexity` tool
  - `PERPLEXITY_MODEL_CHAT`: Overrides default model for `chat_perplexity` tool
  - `DB_PATH`: Custom path for SQLite chat history database (default: chats.db)
- Consult the [Perplexity model docs](https://docs.perplexity.ai/guides/model-cards) for available models
- Use the [mcp-starter](https://github.com/daniel-lxs/mcp-starter) script to easily add this MCP server to Cursor IDE (Currently not working for MacOS).

#### Using Smithery CLI

Smithery is a CLI tool that allows you to easily add MCP servers to your Cursor IDE.

Replace the values of the configuration object with your own values.

```bash
npx -y @smithery/cli@latest run @daniel-lxs/mcp-perplexity --config "{\"perplexityApiKey\":\"abc\",\"perplexityModel\":\"sonar-pro\", \"modelAsk\":\"sonar-pro\", \"modelChat\":\"sonar-reasoning-pro\", \"dbPath\":\"path/to/custom.db\"}"
```

- `perplexityApiKey`: `PERPLEXITY_API_KEY`
- `perplexityModel`: `PERPLEXITY_MODEL`
- `modelAsk`: `PERPLEXITY_MODEL_ASK`
- `modelChat`: `PERPLEXITY_MODEL_CHAT`
- `dbPath`: `DB_PATH`


