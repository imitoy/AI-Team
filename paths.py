"""Path manager — wraps platformdirs with environment variable overrides.

Directory precedence (highest to lowest):
    1. Project-specific env var: AI_TEAM_DATA_DIR, AI_TEAM_CONFIG_DIR, etc.
    2. XDG standard env var: XDG_DATA_HOME, XDG_CONFIG_HOME, etc.
    3. platformdirs system-appropriate default

Usage:
    from paths import paths
    config = paths.config_dir     # ~/.config/ai-team  (or $XDG_CONFIG_HOME/ai-team, etc.)
    data   = paths.data_dir       # ~/.local/share/ai-team
    logs   = paths.log_dir        # ~/.local/state/ai-team/log
    paths.ensure_all()            # create all dirs
"""

from __future__ import annotations

import os
import platformdirs

APP_NAME = "ai-team"
APP_AUTHOR = "ai-team"


class PathManager:
    """Managed access to standard directory paths with env var overrides."""

    def __init__(self, app_name: str = APP_NAME):
        self._app_name = app_name

    # ------------------------------------------------------------------
    # Read-only paths (no auto-create, used for locating existing data)
    # ------------------------------------------------------------------

    def _resolve(self, xdg_var: str, project_var: str, default_fn) -> str:
        """Resolve a directory path with env var precedence."""
        # Project-specific env var wins
        val = os.environ.get(project_var, "")
        if val:
            return val

        # XDG standard env var
        val = os.environ.get(xdg_var, "")
        if val:
            return os.path.join(val, self._app_name)

        # platformdirs default
        return str(default_fn(self._app_name, APP_AUTHOR))

    @property
    def config_dir(self) -> str:
        """Config directory (~/.config/ai-team)."""
        return self._resolve(
            "XDG_CONFIG_HOME", "AI_TEAM_CONFIG_DIR",
            platformdirs.user_config_dir)

    @property
    def data_dir(self) -> str:
        """Data directory (~/.local/share/ai-team)."""
        return self._resolve(
            "XDG_DATA_HOME", "AI_TEAM_DATA_DIR",
            platformdirs.user_data_dir)

    @property
    def cache_dir(self) -> str:
        """Cache directory (~/.cache/ai-team)."""
        return self._resolve(
            "XDG_CACHE_HOME", "AI_TEAM_CACHE_DIR",
            platformdirs.user_cache_dir)

    @property
    def state_dir(self) -> str:
        """State directory (~/.local/state/ai-team)."""
        return self._resolve(
            "XDG_STATE_HOME", "AI_TEAM_STATE_DIR",
            platformdirs.user_state_dir)

    @property
    def log_dir(self) -> str:
        """Log directory (~/.local/state/ai-team/log)."""
        return os.path.join(self.state_dir, "log")

    @property
    def runtime_dir(self) -> str:
        """Runtime directory ($XDG_RUNTIME_DIR/ai-team or /tmp/ai-team-runtime)."""
        val = os.environ.get("AI_TEAM_RUNTIME_DIR", "")
        if val:
            return val
        return str(platformdirs.user_runtime_dir(self._app_name, APP_AUTHOR,
                                                    ensure_exists=False))

    # ------------------------------------------------------------------
    # Derived convenience paths
    # ------------------------------------------------------------------

    @property
    def tools_dir(self) -> str:
        """User-installed tools directory."""
        return os.path.join(self.data_dir, "tools")

    @property
    def mcp_config_path(self) -> str:
        """Path to mcp_servers.json."""
        return os.path.join(self.config_dir, "mcp_servers.json")

    @property
    def history_path(self) -> str:
        """Path to conversation history."""
        return os.path.join(self.state_dir, "history.jsonl")

    @property
    def log_path(self) -> str:
        """Path to the main log file."""
        return os.path.join(self.log_dir, "ai-team.log")

    # ------------------------------------------------------------------
    # Directory creation
    # ------------------------------------------------------------------

    def ensure(self, *dirs: str):
        """Ensure one or more directories exist."""
        for d in dirs:
            os.makedirs(d, exist_ok=True)

    def ensure_all(self):
        """Create all managed directories if they don't exist."""
        self.ensure(
            self.config_dir,
            self.data_dir,
            self.cache_dir,
            self.state_dir,
            self.log_dir,
            self.tools_dir,
        )

    # ------------------------------------------------------------------
    # Listing
    # ------------------------------------------------------------------

    def list_all(self) -> dict[str, str]:
        """Return all path mappings for display or debugging."""
        return {
            "config_dir": self.config_dir,
            "data_dir": self.data_dir,
            "cache_dir": self.cache_dir,
            "state_dir": self.state_dir,
            "log_dir": self.log_dir,
            "runtime_dir": self.runtime_dir,
            "tools_dir": self.tools_dir,
            "mcp_config_path": self.mcp_config_path,
            "history_path": self.history_path,
            "log_path": self.log_path,
        }


# Singleton
paths = PathManager()
