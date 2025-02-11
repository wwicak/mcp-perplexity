@echo off
setlocal EnableDelayedExpansion

echo MCP-Starter Installation Script
echo ------------------------------

:: Check if curl is available
where curl >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: curl is not installed. Please install curl first.
    exit /b 1
)

:: Check if PowerShell is available
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: PowerShell is not installed. Please install PowerShell first.
    exit /b 1
)

:: Install uvx if not present
where uvx >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing uvx...
    powershell -Command "& {Invoke-WebRequest -Uri https://github.com/astral-sh/uv/releases/download/0.1.24/uv-installer.ps1 -OutFile $env:TEMP\uv-installer.ps1; & $env:TEMP\uv-installer.ps1}"
) else (
    echo uvx is already installed
)

:: Create installation directory
if not exist "%USERPROFILE%\.local\bin" mkdir "%USERPROFILE%\.local\bin"

:: Download mcp-starter
echo Downloading mcp-starter...

:: Determine architecture
wmic os get osarchitecture | find "64-bit" >nul
if %ERRORLEVEL% EQU 0 (
    set ARCH=amd64
) else (
    set ARCH=386
)

:: Download the latest release
set DOWNLOAD_URL=https://github.com/daniel-lxs/mcp-starter/releases/latest/download/mcp-starter-windows-%ARCH%.exe
curl -L "%DOWNLOAD_URL%" -o "%USERPROFILE%\.local\bin\mcp-starter.exe"

echo mcp-starter has been installed to %USERPROFILE%\.local\bin\mcp-starter.exe

:: Create configuration
echo Let's configure your MCP server

:: Pre-set command and args as per README
set COMMAND=uvx
set ARGS=mcp-perplexity
set ARGS_JSON=["mcp-perplexity"]

echo Required environment variables:
set /p PERPLEXITY_API_KEY=Enter your Perplexity API key: 
set /p PERPLEXITY_MODEL=Enter Perplexity model (default: sonar-pro): 
if "%PERPLEXITY_MODEL%"=="" set PERPLEXITY_MODEL=sonar-pro

echo Optional environment variables (press enter to skip):
set /p PERPLEXITY_MODEL_ASK=Enter specific model for ask_perplexity (default: same as PERPLEXITY_MODEL): 
set /p PERPLEXITY_MODEL_CHAT=Enter specific model for chat_perplexity (default: same as PERPLEXITY_MODEL): 
set /p DB_PATH=Enter custom DB path (default: chats.db): 

:: Initialize env object with required variables
for /f "delims=" %%i in ('powershell -Command "@{PERPLEXITY_API_KEY='%PERPLEXITY_API_KEY%';PERPLEXITY_MODEL='%PERPLEXITY_MODEL%'} | ConvertTo-Json -Compress"') do set ENV_VARS=%%i

:: Add optional variables if provided
if not "%PERPLEXITY_MODEL_ASK%"=="" (
    for /f "delims=" %%i in ('powershell -Command "$env = '%ENV_VARS%' | ConvertFrom-Json; $env | Add-Member -NotePropertyName 'PERPLEXITY_MODEL_ASK' -NotePropertyValue '%PERPLEXITY_MODEL_ASK%' -Force; $env | ConvertTo-Json -Compress"') do set ENV_VARS=%%i
)
if not "%PERPLEXITY_MODEL_CHAT%"=="" (
    for /f "delims=" %%i in ('powershell -Command "$env = '%ENV_VARS%' | ConvertFrom-Json; $env | Add-Member -NotePropertyName 'PERPLEXITY_MODEL_CHAT' -NotePropertyValue '%PERPLEXITY_MODEL_CHAT%' -Force; $env | ConvertTo-Json -Compress"') do set ENV_VARS=%%i
)
if not "%DB_PATH%"=="" (
    for /f "delims=" %%i in ('powershell -Command "$env = '%ENV_VARS%' | ConvertFrom-Json; $env | Add-Member -NotePropertyName 'DB_PATH' -NotePropertyValue '%DB_PATH%' -Force; $env | ConvertTo-Json -Compress"') do set ENV_VARS=%%i
)

:: Create config directory
if not exist "%USERPROFILE%\.config\mcp-starter" mkdir "%USERPROFILE%\.config\mcp-starter"

:: Create config file using PowerShell
powershell -Command "$config = @{mcpServers=@{mcp-perplexity=@{command='%COMMAND%';args=%ARGS_JSON%;env=$('%ENV_VARS%' | ConvertFrom-Json)}}} | ConvertTo-Json -Depth 10; Set-Content -Path '%USERPROFILE%\.config\mcp-starter\config.json' -Value $config"

echo Configuration file created at: %USERPROFILE%\.config\mcp-starter\config.json
echo To use with Cursor, copy this command:
echo %USERPROFILE%\.local\bin\mcp-starter.exe %USERPROFILE%\.config\mcp-starter\config.json

echo Installation complete! 