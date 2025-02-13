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
- **list_chats_perplexity**: Lists all available chat conversations with Perplexity AI. Returns chat IDs, titles, and creation dates (displayed in relative time format, e.g., "5 minutes ago", "2 days ago"). Results are paginated with 50 chats per page.
- **read_chat_perplexity**: Retrieves the complete conversation history for a specific chat. Returns the full chat history with all messages and their timestamps. No API calls are made to Perplexity - this only reads from local storage.

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

#### Automated Installation

We provide automated installation scripts that will:
1. Install uvx if not present
2. Download and install mcp-starter
3. Guide you through creating the configuration file

<details>
<summary><h5>Windows Installation</h5></summary>

1. Download the `install.ps1` script
2. Open PowerShell as Administrator
3. Allow script execution and run:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\install.ps1
```

The script will:
- Check for required dependencies (curl, PowerShell)
- Install uvx if not present
- Install mcp-starter to `%USERPROFILE%\.local\bin`
- Create a configuration file at `%USERPROFILE%\.config\mcp-starter\config.json`
- Prompt for your Perplexity API key and model preferences
</details>

<details>
<summary><h5>Unix Installation (Linux/MacOS)</h5></summary>

1. Download the `install.sh` script
2. Open Terminal
3. Navigate to the directory containing the script
4. Make the script executable and run it:
```bash
chmod +x install.sh  # Only needed if downloaded directly from browser
./install.sh
```

The script will:
- Check for required dependencies (curl)
- Install uvx if not present
- Install mcp-starter to `$HOME/.local/bin`
- Create a configuration file at `$HOME/.config/mcp-starter/config.json`
- Prompt for your Perplexity API key and model preferences
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
- Use the [mcp-starter](https://github.com/daniel-lxs/mcp-starter) script to easily add this MCP server to Cursor IDE.

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


## Usage

### ask_perplexity

The `ask_perplexity` tool is used for specific questions, this tool doesn't maintain a chat history, every request is a new chat.

The tool will return a response from Perplexity AI using the `PERPLEXITY_MODEL_ASK` model if specified, otherwise it will use the `PERPLEXITY_MODEL` model.

### chat_perplexity

The `chat_perplexity` tool is used for ongoing conversations, this tool maintains a chat history.
A chat is identified by a chat ID, this ID is returned by the tool when a new chat is created. Chat IDs look like this: `wild-horse-12`.

This tool is useful for debugging, research, and any other task that requires a chat history.

The tool will return a response from Perplexity AI using the `PERPLEXITY_MODEL_CHAT` model if specified, otherwise it will use the `PERPLEXITY_MODEL` model.

### list_chats_perplexity
Lists all available chat conversations.  It returns a paginated list of chats, showing the chat ID, title, and creation time (in relative format).  You can specify the page number using the `page` argument (defaults to 1, with 50 chats per page).

### read_chat_perplexity
Retrieves the complete conversation history for a given `chat_id`.  This tool returns all messages in the chat, including timestamps and roles (user or assistant). This tool does *not* make any API calls to Perplexity; it only reads from the local database.







