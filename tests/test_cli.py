import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "mini_agent.cli", *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=ROOT, env=ENV,
    )


def test_help_lists_chat():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "chat" in result.stdout


def test_version():
    result = run_cli("--version")
    assert "mini-agent" in result.stdout


def test_no_args_prints_help():
    result = run_cli()
    assert result.returncode == 0
    assert "chat" in result.stdout