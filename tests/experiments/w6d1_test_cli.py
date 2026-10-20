import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Windows 上子进程 stdout 默认不是 UTF-8 —— 显式声明，避免中文乱码
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "mini_agent.cli", *args],
        capture_output=True,
        text=True, encoding="utf-8", errors="replace",
        cwd=ROOT, env=ENV,
    )


# ── 1. --help ──
result = run_cli("--help")
print(result.stdout)
assert result.returncode == 0
assert "chat" in result.stdout
print()

# ── 2. --version ──
result = run_cli("--version")
print(result.stdout.strip())
assert "mini-agent" in result.stdout
print()

# ── 3. 无参数：打印帮助，不是报错 ──
result = run_cli()
assert result.returncode == 0
assert "chat" in result.stdout
print("✓ CLI 骨架全部场景通过")