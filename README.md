# Perplexity MCP Server

[![smithery badge](https://smithery.ai/badge/@daniel-lxs/mcp-perplexity)](https://smithery.ai/server/@daniel-lxs/mcp-perplexity)

MCP Server for the Perplexity API.

<a href="https://glama.ai/mcp/servers/hchfq9bydq"><img width="380" height="200" src="https://glama.ai/mcp/servers/hchfq9bydq/badge" alt="Perplexity Server MCP server" /></a>

## Components

### Tools

- **ask_perplexity**: Request expert programming assistance through Perplexity. Focuses on coding solutions, error debugging, and technical explanations. Returns responses with source citations and alternative suggestions.

## Key Features

- **Streaming Responses with Progress Reporting:**  Provides a more interactive experience by streaming responses and reporting progress during long queries.
- **Simplified Tool Parameters:** The `ask_perplexity` tool now only requires a `query` parameter, simplifying its usage.
- **Model Configuration via Environment Variable:**  Allows you to specify the Perplexity model using the `PERPLEXITY_MODEL` environment variable for flexible model selection.
- **Improved Error Handling and Robustness:** Incorporates better error handling and more robust API interaction.


## Quickstart

### Installation

#### Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [pipx](https://pipx.pypa.io/stable/)

#### Install the MCP Server

You have two options to install the MCP server. **For the latest version, it is recommended to install from the repository:**

**1. Install locally for development (Recommended for latest version):**

To ensure you have the most up-to-date version with the latest features and fixes, install from the GitHub repository.

```bash
# Clone the repository
git clone https://github.com/daniel-lxs/mcp-perplexity.git
cd mcp-perplexity

# Build the package
hatch build

# Install using pipx from the local distribution
pipx install dist/mcp_perplexity-0.2.5-py3-none-any.whl
```

**Explanation for local development install:**

- `hatch build`: This command uses `hatch` (the build system specified in `pyproject.toml`) to build the package. It creates a distribution-ready `.whl` file in the `dist` directory.
- `pipx install dist/mcp_perplexity-0.2.5-py3-none-any.whl`: This command then installs the server using `pipx` from the locally built `.whl` file. This ensures you are running the code from your local development environment.

**2. Install directly from PyPI (Potentially outdated):**

This method installs the released version from the Python Package Index.  **Note that this version might not be the most current.**

```bash
pipx install mcp-perplexity
```


#### Configure your MCP Client

To use this MCP server, you need to configure your MCP client to connect to it.  The configuration method will vary depending on your specific client.

Below is an example configuration in JSON format.  **Refer to your MCP client's documentation for the exact configuration steps and format.**

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
- The `"PERPLEXITY_MODEL": "sonar-pro"` line is optional. If you omit it, the server will use the default Perplexity model.  You can change `"sonar-pro"` to other supported models if needed.
- Consult your MCP client's documentation for details on where to place this configuration and any client-specific settings.
