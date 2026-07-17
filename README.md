# AI-Team — Multi-Role AI Agent Team

A Python framework that simulates a full software development team using multiple AI roles — Architect, Coder, Organizer, Reviewer, Security, Tester — each with tailored system prompts and tool sets. Roles coordinate via tool calling (function calling) to automate complex software engineering tasks.

## Key Features

- **6 roles**: Architect, Coder, Organizer, Reviewer, Security, Tester
- **26 built-in tools**: file I/O, shell commands, glob/grep search, browser automation, MCP support
- **Multi-provider**: DeepSeek, GLM (Zhipu), OpenRouter (4 providers, 10 models)
- **Inter-role delegation**: `call_role_*` tools let roles delegate tasks to each other
- **Browser tools**: web navigation via `agent-browser` (accessibility tree snapshots)
- **MCP integration**: connect to MCP servers to discover and use external tools dynamically
- **Auto MR script**: `scripts/create-mr.py` for automated GitLab merge requests

## Quick Start

### Requirements

- Python 3.10+
- pip

### Install

```bash
cd AI-Team
pip install -e .
# or just:
pip install openai zhipuai mcp
```

### Set API Key

```bash
export DEEPSEEK_API_KEY="sk-..."
export GLM_API_KEY="your-glm-key"          # optional
export OPENROUTER_API_KEY="sk-or-..."      # optional
```

### Run

```bash
python3 main.py
```

The Organizer role will greet you. Describe your project and the team coordinates automatically.

### Non-interactive mode (skip approval prompts)

```bash
AI_TEAM_AUTO_APPROVE=1 python3 main.py
```

## Project Structure

```
AI-Team/
├── main.py                  # REPL entry point
├── roles.py                 # 6 role definitions (name, system_prompt, tools)
├── communication.py         # Communication manager, AskProceed, role delegation
│
├── provider/                # Model provider definitions
│   ├── __init__.py          # Auto-loads all providers, merges into MODELS
│   ├── deepseek.py          # DeepSeek V4 (3 models)
│   ├── glm.py               # GLM/Zhipu (3 models)
│   └── openrouter.py        # OpenRouter (4 models)
│
├── api/                     # API backends
│   ├── __init__.py          # Factory: create_api(model_key, role_name)
│   ├── openai.py            # OpenAIAPI — OpenAI-compatible endpoints
│   └── glm.py               # GLMAPI — Zhipu SDK with thinking mode support
│
├── tools/                   # Tool implementations
│   ├── __init__.py          # Tool registry (auto-discovery)
│   ├── read_file.py         # Read file
│   ├── write_file.py        # Write file
│   ├── edit_file.py         # Edit file (find-and-replace)
│   ├── run_command.py       # Shell command execution
│   ├── list_files.py        # List directory recursively
│   ├── glob_files.py        # Find files by glob pattern
│   ├── grep_search.py       # Search file contents by regex
│   ├── read_architect.py    # Read ARCHITECT.md
│   ├── write_architect.py   # Write ARCHITECT.md
│   ├── get_weather.py       # Mock weather lookup (testing)
│   ├── kill_process.py      # Kill detached process
│   ├── call_role.py         # 6 call_role_* tools (dynamic)
│   ├── browser_navigate.py  # Navigate to URL
│   ├── browser_snapshot.py  # Get page accessibility tree
│   ├── browser_click.py     # Click element by ref
│   ├── browser_type.py      # Type into input
│   ├── browser_scroll.py    # Scroll page
│   ├── browser_back.py      # Go back in history
│   ├── browser_press.py     # Press keyboard key
│   ├── browser_console.py   # Get console/JS errors
│   ├── browser.py           # agent-browser CLI wrapper
│   └── mcp/                 # MCP client
│       └── __init__.py      # MCPManager, stdio/HTTP transport
│
├── scripts/
│   ├── create-mr.py         # Auto GitLab MR creator
│   └── setup-git-hook.sh    # Install git post-push hook
│
└── pyproject.toml
```

## Providers & Models

| Provider | api_type | Models |
|----------|----------|--------|
| DeepSeek | openai | `deepseek-v4-flash`, `deepseek-v4`, `deepseek-reasoner` |
| OpenRouter | openai | `deepseek/deepseek-v4-flash`, `anthropic/claude-sonnet-4`, `openai/gpt-4o`, `google/gemini-2-pro` |
| GLM | glm | `glm-5`, `glm-5-flash`, `glm-4-air` |

Configure in `provider/<name>.py`. Each provider defines `PROVIDER` dict with `api_type`, `base_url`, `env_key`, `api_key`, and `models`.

## Tools by Role

| Role | Tools | Count |
|------|-------|-------|
| Architect | read_architect, write_architect, glob_files, grep_search, read_file, 8 browser, call_role | 14 |
| Coder | read_file, write_file, edit_file, run_command, glob_files, grep_search, 8 browser, call_role | 15 |
| Organizer | call_role, 7 browser (no browser_console) | 8 |
| Reviewer | read_file, glob_files, grep_search, 8 browser, call_role | 12 |
| Security | read_file, run_command, glob_files, grep_search, 8 browser, call_role | 13 |
| Tester | read_file, run_command, glob_files, grep_search, 8 browser, call_role | 13 |

## MCP Support

AI-Team can connect to MCP (Model Context Protocol) servers to discover and use external tools. Configure servers in `mcp_servers.json`:

```json
{
    "time": {
        "command": "uvx",
        "args": ["mcp-server-time"]
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
        }
    },
    "my_api": {
        "url": "https://mcp.example.com/mcp",
        "headers": {
            "Authorization": "Bearer sk-..."
        }
    }
}
```

MCP tools are registered as `mcp_{server}_{tool}` (e.g., `mcp_time_get_current_time`).

## Auto MR Script

```bash
# Create MR from current branch to upstream
python3 scripts/create-mr.py

# With custom title
python3 scripts/create-mr.py --source feat-branch --title "My feature"

# Install auto-MR on every push
bash scripts/setup-git-hook.sh
```

## Configuration

| Env Variable | Description |
|-------------|-------------|
| `DEEPSEEK_API_KEY` | DeepSeek API key |
| `GLM_API_KEY` / `ZHIPUAI_API_KEY` | GLM/Zhipu API key |
| `OPENROUTER_API_KEY` | OpenRouter API key |
| `AI_TEAM_AUTO_APPROVE` | Set to `1` to skip tool approval prompts |
| `MCP_SERVERS_JSON` | JSON string of MCP server configs |

## License

MIT License — see [LICENSE](LICENSE)
