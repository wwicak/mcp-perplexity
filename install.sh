#!/bin/bash
set -e  # Exit immediately on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}MCP-Starter Installation Script${NC}"
echo "--------------------------------"

# Check prerequisites
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is required but not installed.${NC}"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required but not installed.${NC}"
    exit 1
fi

# Function to install uvx if not present
install_uvx() {
    if ! command -v uvx &> /dev/null; then
        echo -e "${BLUE}Installing uvx...${NC}"
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
        
        # Verify installation
        if ! command -v uvx &> /dev/null; then
            echo -e "${RED}Error: uvx installation failed. Check ~/.local/bin/uvx exists${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}uvx is already installed${NC}"
    fi
}

# Function to download mcp-starter
download_mcp_starter() {
    echo -e "${BLUE}Downloading mcp-starter...${NC}"
    
    # Determine system architecture
    ARCH=$(uname -m)
    case "$ARCH" in
        x86_64) ARCH="amd64" ;;
        aarch64) ARCH="arm64" ;;
        *)
            echo -e "${RED}Unsupported architecture: $ARCH${NC}"
            exit 1
            ;;
    esac
    
    # Determine OS
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    
    # Create temporary directory
    TMP_DIR=$(mktemp -d)
    trap 'rm -rf "$TMP_DIR"' EXIT  # Cleanup on exit
    
    # Download the latest release
    DOWNLOAD_URL="https://github.com/daniel-lxs/mcp-starter/releases/latest/download/mcp-starter-${OS}-${ARCH}"
    if ! curl -L "$DOWNLOAD_URL" -o "$TMP_DIR/mcp-starter"; then
        echo -e "${RED}Error: Failed to download mcp-starter${NC}"
        exit 1
    fi
    
    # Make it executable
    chmod +x "$TMP_DIR/mcp-starter"
    
    # Move to permanent location
    mkdir -p "$HOME/.local/bin"
    if ! mv "$TMP_DIR/mcp-starter" "$HOME/.local/bin/"; then
        echo -e "${RED}Error: Failed to install mcp-starter${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}mcp-starter has been installed to $HOME/.local/bin/mcp-starter${NC}"
}

# Function to create configuration
create_config() {
    echo -e "${BLUE}Let's configure your MCP server${NC}"
    
    # Pre-set command and args as per README
    COMMAND="uvx"
    ARGS="mcp-perplexity"
    ARGS_JSON="[\"mcp-perplexity\"]"
    
    echo -e "${BLUE}Required environment variables:${NC}"
    read -p "Enter your Perplexity API key: " PERPLEXITY_API_KEY
    read -p "Enter Perplexity model (default: sonar-pro): " PERPLEXITY_MODEL
    PERPLEXITY_MODEL=${PERPLEXITY_MODEL:-sonar-pro}
    
    echo -e "${BLUE}Optional environment variables (press enter to skip):${NC}"
    read -p "Enter specific model for ask_perplexity (default: same as PERPLEXITY_MODEL): " PERPLEXITY_MODEL_ASK
    read -p "Enter specific model for chat_perplexity (default: same as PERPLEXITY_MODEL): " PERPLEXITY_MODEL_CHAT
    read -p "Enter custom DB path (default: chats.db): " DB_PATH
    
    # Initialize env object with required variables
    ENV_VARS=$(echo "{}" | jq --arg k "PERPLEXITY_API_KEY" --arg v "$PERPLEXITY_API_KEY" '. + {($k): $v}')
    ENV_VARS=$(echo "$ENV_VARS" | jq --arg k "PERPLEXITY_MODEL" --arg v "$PERPLEXITY_MODEL" '. + {($k): $v}')
    
    # Add optional variables if provided
    if [ ! -z "$PERPLEXITY_MODEL_ASK" ]; then
        ENV_VARS=$(echo "$ENV_VARS" | jq --arg k "PERPLEXITY_MODEL_ASK" --arg v "$PERPLEXITY_MODEL_ASK" '. + {($k): $v}')
    fi
    if [ ! -z "$PERPLEXITY_MODEL_CHAT" ]; then
        ENV_VARS=$(echo "$ENV_VARS" | jq --arg k "PERPLEXITY_MODEL_CHAT" --arg v "$PERPLEXITY_MODEL_CHAT" '. + {($k): $v}')
    fi
    if [ ! -z "$DB_PATH" ]; then
        ENV_VARS=$(echo "$ENV_VARS" | jq --arg k "DB_PATH" --arg v "$DB_PATH" '. + {($k): $v}')
    fi
    
    # Create the config file
    CONFIG_FILE="$HOME/.config/mcp-starter/config.json"
    mkdir -p "$(dirname "$CONFIG_FILE")"
    
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "mcp-perplexity": {
      "command": "$COMMAND",
      "args": $ARGS_JSON,
      "env": $ENV_VARS
    }
  }
}
EOF
    
    echo -e "${GREEN}Configuration file created at: $CONFIG_FILE${NC}"
    echo -e "${BLUE}To use with Cursor, copy this command:${NC}"
    echo -e "${GREEN}$HOME/.local/bin/mcp-starter $CONFIG_FILE${NC}"
}

# Main installation process
install_uvx
download_mcp_starter
create_config

echo -e "${GREEN}Installation complete!${NC}"
echo -e "${BLUE}Ensure $HOME/.local/bin is in your PATH:${NC}"
echo -e "export PATH=\"\$HOME/.local/bin:\$PATH\"" 