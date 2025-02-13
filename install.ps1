# MCP-Starter Installation Script

# Check if curl is available
if (!(Get-Command curl -ErrorAction SilentlyContinue)) {
    Write-Host "Error: curl is not installed. Please install curl first."
    exit 1
}

# Install uv and uvx if not present
if (!(Get-Command uvx -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv and uvx..."
    try {
        # Install uv using recommended method
        irm https://astral.sh/uv/install.ps1 | iex
        
        # Refresh PATH to include .local/bin
        $localBinPath = Join-Path $env:USERPROFILE ".local\bin"
        $env:Path += ";$localBinPath"
        
        # Verify uv installation
        if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
            Write-Host "uv installation failed. Check if uv.exe exists in: $localBinPath"
            exit 1
        }
        
        # Check if uvx is already installed (since it might be bundled with uv)
        if (!(Get-Command uvx -ErrorAction SilentlyContinue)) {
            Write-Host "uvx is not found after uv installation, attempting to install via pip..."

            # Create and activate virtual environment (using a specific Python version if needed)
            Write-Host "Creating Python virtual environment..."
            if (!(uv venv -p 3.11 .venv)) {
                Write-Host "Failed to create virtual environment. Trying without specifying Python version..."
                uv venv .venv
            }

            # Install uvx in the virtual environment
            Write-Host "Installing uvx..."
            if (!(uv pip install uvx)) {
                Write-Host "Failed to install uvx using 'uv pip install'.  You may need to install it manually."
                exit 1
            }
        } else {
            Write-Host "uvx is already installed with uv."
        }

        # Verify uvx installation (again, after potential pip install)
        if (!(Get-Command uvx -ErrorAction SilentlyContinue)) {
            Write-Host "uvx installation failed. Try restarting your shell to refresh PATH"
            exit 1
        }

    } catch {
        Write-Host "Installation failed: $_"
        Write-Host "Please ensure you have an internet connection and that PowerShell has the necessary permissions."
        exit 1
    }
} else {
    Write-Host "uvx is already installed"
}

# Create installation directory
$installDir = Join-Path $env:USERPROFILE ".local\bin"
if (!(Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force
}

# Download mcp-starter
Write-Host "Downloading mcp-starter..."
try {
    $downloadUrl = "https://github.com/daniel-lxs/mcp-starter/releases/latest/download/mcp-starter-windows-amd64.exe"
    Invoke-WebRequest -Uri $downloadUrl -OutFile (Join-Path $installDir "mcp-starter.exe")
    Write-Host "mcp-starter has been installed to $installDir\mcp-starter.exe"
}
catch {
    Write-Host "Error downloading mcp-starter: $_"
    Write-Host "Please check your internet connection and ensure the GitHub repository is accessible."
    exit 1
}

# Create configuration
Write-Host "Let's configure your MCP server"

# Pre-set command and args as per README
$command = "uvx"
$args = "mcp-perplexity"

Write-Host "Required environment variables:"
$perplexityApiKey = Read-Host "Enter your Perplexity API key"
if ([string]::IsNullOrEmpty($perplexityApiKey)) {
    Write-Host "Error: Perplexity API key cannot be empty."
    exit 1
}
$perplexityModel = Read-Host "Enter Perplexity model (default: sonar-pro)"
if ([string]::IsNullOrEmpty($perplexityModel)) {
    $perplexityModel = "sonar-pro"
}

Write-Host "Optional environment variables (press enter to skip):"
$perplexityModelAsk = Read-Host "Enter specific model for ask_perplexity (default: same as PERPLEXITY_MODEL)"
$perplexityModelChat = Read-Host "Enter specific model for chat_perplexity (default: same as PERPLEXITY_MODEL)"
$dbPath = Read-Host "Enter custom DB path (default: chats.db)"

# Initialize env object with required variables
$envVars = @{
    PERPLEXITY_API_KEY = $perplexityApiKey
    PERPLEXITY_MODEL   = $perplexityModel
}
if (![string]::IsNullOrEmpty($perplexityModelAsk)) {
    $envVars.Add("PERPLEXITY_MODEL_ASK", $perplexityModelAsk)
}
if (![string]::IsNullOrEmpty($perplexityModelChat)) {
    $envVars.Add("PERPLEXITY_MODEL_CHAT", $perplexityModelChat)
}
if (![string]::IsNullOrEmpty($dbPath)) {
    $envVars.Add("DB_PATH", $dbPath)
}

# Create config directory
$configDir = Join-Path $env:USERPROFILE ".config\mcp-starter"
if (!(Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force
}

# Create config file using PowerShell
try {
    $config = @{
        mcpServers = @{
            "mcp-perplexity" = @{
                command = $command
                args    = @($args)  # Array directly in the structure
                env     = $envVars  # Hashtable directly in the structure
            }
        }
    } | ConvertTo-Json -Depth 4  # Proper depth for nesting
    $configPath = Join-Path $configDir "config.json"
    Set-Content -Path $configPath -Value $config -Force

    Write-Host "Configuration file created at: $configPath"
    Write-Host "To use with Cursor, copy this command:"
    Write-Host (Join-Path $installDir "mcp-starter.exe") + " " + $configPath
    Write-Host "Installation complete!"

} catch {
    Write-Host "Error creating configuration file: $_"
    Write-Host "Please ensure you have write permissions to the configuration directory."
    exit 1
}
Write-Host "Please consider adding $localBinPath to your system PATH environment variable for easier access."
