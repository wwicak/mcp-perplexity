# Changelog

All notable changes to this project will be documented in this file.

## v0.4.0 (2025-02-14)

### Features

*   **Chat Functionality**: Added list and read chat functionality for Perplexity conversations.
    *   Implemented `list_chats_perplexity` to retrieve a paginated chat list with details.
    *   Added `read_chat_perplexity` to fetch complete chat history from local storage.
    *   Introduced relative time formatting for chat creation timestamps to aid models without current date/time access.

### Internal

*   Updated semantic release configuration and version tracking.
*   Bumped version to 0.4.0 for the new chat functionality release.

## v0.3.4 (2025-02-13)

### Bug Fixes

*   **Windows Installation**: Simplified Windows architecture detection in the installation script, as it's only available for amd64.

### Documentation

*   Updated README.md with the latest information.

### Internal

*   Bumped project version to 0.3.4.

## v0.3.3 (2025-02-11)

### Features

*   **Installation**: Add cross-platform installation scripts for mcp-starter

### Bug Fixes

*   **Configuration**: Update database path environment variable name to match the documentation.

### Documentation

*   Updated Windows and Unix installation instructions.
*   Added a usage section for the `ask_perplexity` and `chat_perplexity` tools.
*   Updated README with Smithery CLI usage and a macOS note.

### Internal

*   Improved installation scripts with enhanced error handling and user experience.
*   Bumped project version to 0.3.2.

## v0.3.0 (2025-02-10)

### Features

*   **Configuration**: Added configuration options for Perplexity model and chat database (via environment variables).

### Bug Fixes

*   Fixed package naming and versioning issues.

### Refactorings

*   Updated MCP start command and added Dockerfile configuration.
*   Enhanced Dockerfile for development and runtime configuration.
*   Optimized Dockerfile and dependency management (multi-stage build, efficient dependency installation, Hatch build configuration, and `uv.lock` update).

### Documentation

*   Revamped README with a comprehensive installation and configuration guide, including:
    *   Removal of Smithery installation section.
    *   Detailed `uvx` installation instructions for Windows and Unix systems.
    *   Enhanced MCP client configuration documentation.
    *   More detailed environment variable explanations.
    *   A link to Perplexity model documentation.

### CI/CD

*   Enabled manual workflow dispatch for PyPI package publishing in GitHub Actions.

### Build

*   Updated Hatch build configuration for package sources.

### Internal

*   Bumped project version to 0.3.0.

## v0.2.1 (2025-02-06)

### Documentation

*   Updated README with improved feature descriptions and model information.
*   Updated Glama.ai server badge URL in README.
*   Added PyPI publish workflow badge to README.

### Internal

*   Bumped project version to 0.2.1.
*   Updated release workflow permissions configuration in GitHub Actions (moved permissions to top-level, added explicit write permissions).

## v0.2.0 (2025-02-06)

### Features

*   **Database**: Enhanced database initialization with robust error handling and configurable database path via the `PERPLEXITY_DB_PATH` environment variable.

### Bug Fixes

*   Reduced the amount of numbers generated for chat IDs.
*   Removed an invalid property from progress notifications.

### Refactorings

*   Simplified system prompt and improved code formatting. Extracted the system prompt to a constant for reusability.  Reduced code duplication in tool handling methods.

### Internal

*   Updated artifact upload configuration in release workflow (upgraded `actions/upload-artifact`, added retention and compression settings).
*   Optimized GitHub Actions release workflow for semantic release.
*   Improved Hatch installation and verification in GitHub Actions workflow.
*   Adjusted Hatch build and GitHub Actions configuration (explicit Python command, added Hatch to PATH).
*   Updated Hatch GitHub Action to the latest version.
*   Refined release workflow Hatch integration.
*   Updated build and release workflow to use Hatch.
*   Configured semantic release for automated versioning and GitHub releases.
*   Updated VSCode configuration in `.gitignore`.
*   Removed VSCode Python settings file.

### Documentation

*   Updated `mcp-server-starter` reference to `mcp-starter` in the README.

## v0.1.2 (2025-02-05)

### Features

*   **Model Configuration**: Added configurable Perplexity models for `ask` and `chat` tools via `PERPLEXITY_MODEL_ASK` and `PERPLEXITY_MODEL_CHAT` environment variables. Increased chat ID token length for more unique identifiers.

### Documentation

*   Updated README with new Perplexity model configuration details.

### Internal

*   Bumped version to 0.1.2.

## v0.1.1 (2025-02-05)

### Features

*   **Chat Functionality**: Added persistent chat functionality and database storage using SQLite. Implemented a new `chat_perplexity` tool for maintaining conversation context, including chat ID generation and message storage, and enhanced progress tracking.
*   **Streaming Responses**: Enhanced Perplexity tool with streaming response and improved error handling, including refactoring the API interaction, adding robust JSON parsing, and implementing detailed response formatting with a system prompt.

### Bug Fixes

*   Added a note about potential timeouts to the README.

### Testing

*   Added a comprehensive Perplexity API test suite.

### Documentation

*   Updated README with comprehensive installation instructions for the MCP server.
*   Updated MCP client configuration instructions in README.
*   Updated the project repository and README with new features and installation instructions.

### Internal

*   Bumped version to 0.1.1.