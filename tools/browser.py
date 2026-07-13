#!/usr/bin/env python3
"""
Browser backend for AI-Team. Wraps agent-browser CLI for web browsing.
Usage: python3 browser.py <command> [args...]

Commands:
  navigate <url>         Navigate to URL
  snapshot [--full]      Get page accessibility snapshot (compact by default)
  click <ref>            Click element by ref (e.g., @e5)
  type <ref> <text>      Clear and type into element
  scroll <direction>     Scroll up/down
  back                   Go back in history
  press <key>            Press keyboard key (Enter, Tab, Escape, etc.)
  console [--clear]      Get console messages and JS errors
  images                 List images on page
  close                  Close browser session

All output is JSON on stdout: {"success": true/false, ...}
"""

import json
import shutil
import subprocess
import sys
import os
import tempfile
import time

# Unique session name for AI-Team browser persistence
SESSION_NAME = "ai-team-browser"


def find_agent_browser() -> str:
    """Find agent-browser CLI, preferring local installs."""
    # Check if npx can find it
    npx = shutil.which("npx")
    if npx:
        try:
            result = subprocess.run(
                [npx, "agent-browser", "--version"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return "npx agent-browser"
        except (subprocess.TimeoutExpired, OSError):
            pass
    raise FileNotFoundError(
        "agent-browser not found. Install with: npm install -g agent-browser"
    )


def run_agent_browser(command: str, args: list = None, timeout: int = 30) -> dict:
    """Run an agent-browser command and return parsed JSON."""
    args = args or []
    cmd = f"npx agent-browser --session {SESSION_NAME} --json {command} {' '.join(quote_arg(a) for a in args)}"

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, shell=True
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stdout:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "content": stdout,
                    "raw_stderr": stderr,
                }
        else:
            return {
                "success": False,
                "error": stderr or "No output from agent-browser",
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Command timed out after {timeout}s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def quote_arg(arg: str) -> str:
    """Shell-quote a single argument."""
    if not arg or any(c in arg for c in (' ', '"', "'", '\\', '$', '`')):
        escaped = arg.replace("'", "'\\''")
        return "'" + escaped + "'"
    return arg


def cmd_navigate(args: list) -> str:
    if not args:
        return json.dumps({"success": False, "error": "URL required"})
    url = args[0]
    result = run_agent_browser("open", [url], timeout=60)
    if result.get("success"):
        data = result.get("data", {})
        response = {
            "success": True,
            "title": data.get("title", ""),
            "url": data.get("url", url),
        }

        # Auto-take compact snapshot after navigation
        try:
            snap = run_agent_browser("snapshot", ["-c"])
            if snap.get("success"):
                snap_data = snap.get("data", {})
                response["snapshot"] = snap_data.get("snapshot", "")
                refs = snap_data.get("refs", {})
                response["element_count"] = len(refs) if refs else 0
        except Exception:
            pass

        return json.dumps(response, ensure_ascii=False)
    else:
        return json.dumps({
            "success": False,
            "error": result.get("error", "Navigation failed"),
        }, ensure_ascii=False)


def cmd_snapshot(args: list) -> str:
    cmd_args = []
    for a in args:
        if a in ("--full", "-f"):
            pass  # full mode — no -c flag
        else:
            cmd_args.append(a)
    if "--full" not in args and "-f" not in args:
        cmd_args.insert(0, "-c")  # compact mode by default

    result = run_agent_browser("snapshot", cmd_args)
    if result.get("success"):
        data = result.get("data", {})
        snapshot_text = data.get("snapshot", "")
        refs = data.get("refs", {})

        # Truncate very long snapshots
        if len(snapshot_text) > 8000:
            snapshot_text = snapshot_text[:8000] + "\n... [truncated]"

        response = {
            "success": True,
            "snapshot": snapshot_text,
            "element_count": len(refs) if refs else 0,
        }
        return json.dumps(response, ensure_ascii=False)
    else:
        return json.dumps({
            "success": False,
            "error": result.get("error", "Failed to get snapshot"),
        }, ensure_ascii=False)


def cmd_click(args: list) -> str:
    if not args:
        return json.dumps({"success": False, "error": "Element ref required"})
    ref = args[0]
    if not ref.startswith("@"):
        ref = f"@{ref}"
    result = run_agent_browser("click", [ref])
    if result.get("success"):
        return json.dumps({"success": True, "clicked": ref}, ensure_ascii=False)
    else:
        return json.dumps({
            "success": False,
            "error": result.get("error", f"Failed to click {ref}"),
        }, ensure_ascii=False)


def cmd_type(args: list) -> str:
    if len(args) < 2:
        return json.dumps({
            "success": False,
            "error": "Usage: type <ref> <text>",
        })
    ref = args[0]
    text = " ".join(args[1:])
    if not ref.startswith("@"):
        ref = f"@{ref}"
    result = run_agent_browser("fill", [ref, text])
    if result.get("success"):
        return json.dumps({
            "success": True,
            "typed": text,
            "element": ref,
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "success": False,
            "error": result.get("error", f"Failed to type into {ref}"),
        }, ensure_ascii=False)


def cmd_scroll(args: list) -> str:
    if not args or args[0] not in ("up", "down"):
        return json.dumps({
            "success": False,
            "error": "Usage: scroll up|down",
        })
    direction = args[0]
    SCROLL_PIXELS = 500
    result = run_agent_browser("scroll", [direction, str(SCROLL_PIXELS)])
    if result.get("success"):
        return json.dumps({"success": True, "scrolled": direction}, ensure_ascii=False)
    else:
        return json.dumps({
            "success": False,
            "error": result.get("error", f"Failed to scroll {direction}"),
        }, ensure_ascii=False)


def cmd_back(args: list) -> str:
    result = run_agent_browser("back", [])
    if result.get("success"):
        data = result.get("data", {})
        return json.dumps({
            "success": True,
            "url": data.get("url", ""),
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "success": False,
            "error": result.get("error", "Failed to go back"),
        }, ensure_ascii=False)


def cmd_press(args: list) -> str:
    if not args:
        return json.dumps({"success": False, "error": "Key name required"})
    key = args[0]
    result = run_agent_browser("press", [key])
    if result.get("success"):
        return json.dumps({"success": True, "pressed": key}, ensure_ascii=False)
    else:
        return json.dumps({
            "success": False,
            "error": result.get("error", f"Failed to press {key}"),
        }, ensure_ascii=False)


def cmd_console(args: list) -> str:
    clear = "--clear" in args
    console_args = ["--clear"] if clear else []

    console_result = run_agent_browser("console", console_args)
    errors_result = run_agent_browser("errors", console_args)

    messages = []
    if console_result.get("success"):
        for msg in console_result.get("data", {}).get("messages", []):
            messages.append({
                "type": msg.get("type", "log"),
                "text": msg.get("text", ""),
                "source": "console",
            })

    errors = []
    if errors_result.get("success"):
        for err in errors_result.get("data", {}).get("errors", []):
            errors.append({
                "message": err.get("message", ""),
                "source": "exception",
            })

    response = {
        "success": True,
        "console_messages": messages,
        "js_errors": errors,
        "total_messages": len(messages),
        "total_errors": len(errors),
    }
    return json.dumps(response, ensure_ascii=False)


def cmd_images(args: list) -> str:
    result = run_agent_browser("images", [])
    if result.get("success"):
        data = result.get("data", {})
        images = data.get("images", [])
        response = {
            "success": True,
            "images": [
                {"url": img.get("src", ""), "alt": img.get("alt", "")}
                for img in images
            ],
            "total": len(images),
        }
        return json.dumps(response, ensure_ascii=False)
    else:
        return json.dumps({"success": True, "images": [], "total": 0},
                          ensure_ascii=False)


def cmd_close(args: list) -> str:
    """Close the browser session."""
    try:
        subprocess.run(
            f"npx agent-browser --session {SESSION_NAME} close",
            capture_output=True, text=True, timeout=10, shell=True
        )
    except Exception:
        pass
    return json.dumps({"success": True, "closed": True}, ensure_ascii=False)


COMMANDS = {
    "navigate": cmd_navigate,
    "snapshot": cmd_snapshot,
    "click": cmd_click,
    "type": cmd_type,
    "scroll": cmd_scroll,
    "back": cmd_back,
    "press": cmd_press,
    "console": cmd_console,
    "images": cmd_images,
    "close": cmd_close,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    handler = COMMANDS.get(command)
    if not handler:
        print(json.dumps({
            "success": False,
            "error": f"Unknown command: {command}. Available: {', '.join(COMMANDS)}",
        }))
        return

    try:
        result = handler(args)
        print(result)
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))


if __name__ == "__main__":
    main()