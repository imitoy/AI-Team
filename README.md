# AI Team — Lua-based Multi-AI Collaboration Framework

AI Team is a lightweight framework (Lua + luapython) that simulates a software development team using multiple AI roles. Each role (project manager, architect, lead, engineer, writer, reviewer) coordinates via structured messages and callable tools to automate project tasks such as task decomposition, file edits, and code review. The project currently uses DeepSeek-compatible APIs but is designed to support OpenAI-compatible endpoints as well.

## Key Features

- Role-based collaboration: distinct AI roles with clear responsibilities.
- Tool execution: safe wrappers for file operations and shell commands.
- Pluggable models: add or switch AI backends in `communication/models.lua`.
- Interactive workflow: prompts user confirmation for sensitive actions.

## Quick Start

Requirements

- Linux (recommended)
- Lua 5.4
- Python 3.x
- luarocks
- Dependencies: `luapython`, `lua-cjson`, `python-openai` (or DeepSeek client)

Install (example for Arch Linux)

```bash
sudo pacman -Syu
sudo pacman -S lua5.4 luarocks python
sudo luarocks install luapython --lua-version 5.4
sudo luarocks install lua-cjson --lua-version 5.4
pip install openai
```

Set API key (example environment variable)

```bash
export DEEPSEEK_APIKEY="your_api_key_here"
```

Run the project

```bash
cd AI-Team.lua || cd .
mkdir -p work
cd work
lua5.4 ../main.lua
```

When prompted, describe the project you want the AI team to implement (for example: "Build a simple Snake game").

## Project Structure

The repository is organized as follows:

```
AI-Team.lua
main.lua
api.lua
communication.lua
models.lua
roles.lua
tools.lua
README.md
```

Key modules

- `main.lua` — program entry point
- `communication.lua` — orchestrates messages between roles
- `models.lua` — model and tool configurations
- `api.lua` — API adapter for OpenAI/DeepSeek-style endpoints
- `tools.lua` — implementations of callable tools (file ops, commands)

## Roles

The system defines several cooperating roles (configured in `communication/avatar.lua`):

- Project Manager: translates user goals into tasks and priorities.
- System Architect: produces high-level designs and component interactions.
- Development Lead: decomposes tasks into file-level work and assigns engineers.
- Development Engineer: performs file edits and implements features.
- Documentation Writer: produces project documentation.
- Code Reviewer: inspects code and provides suggestions.

## Configuration & Extensibility

- Add or modify roles in `communication/avatar.lua`.
- Add tools or change their behavior in `communication/models.lua` (see the `tools` array).
- Add new model entries (base URL, auth, models, tools) in `communication/models.lua` to support additional AI backends.

Example tool entry (conceptual):

```lua
{
  name = "write_file",
  description = "Create or overwrite a file",
  action = function(params) -- params: {path = "", content = ""}
    -- implement safe write
  end
}
```

## Safety and Costs

- API usage may incur costs; monitor usage and set quotas where possible.
- The framework can run file and shell operations — review prompts carefully before confirming.

## Contributing

1. Open an issue describing your feature or bug.
2. Fork the repo and create a branch for your changes.
3. Add tests or a reproducible demo when relevant.

## License

This project is released under the MIT License.

## Contact

- Repository: https://github.com/imitoy/AI-Team
- Issues: use GitHub Issues in the repo
- Author: root@imitoy.top
