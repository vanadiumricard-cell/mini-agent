from pathlib import Path
from mini_agent.tools.base import Tool
PROJECT_ROOT=Path(__file__).resolve().parents[3]
class ReadFileTool(Tool):
    name = "read_file"
    description = "读取项目内的一个文本文件并返回其内容"
    parameters = {
        "path": {
            "type": "string",
            "description": "文件路径（相对于项目根目录，例如 src/mini_agent/agent.py）",
        },
    }
    required = ["path"]

    def run(self, path):
        file_path = (PROJECT_ROOT / path).resolve()
        if not file_path.is_relative_to(PROJECT_ROOT):
            return f"错误：拒绝访问项目目录之外的文件：{path}"
        if not file_path.exists():
            return f"错误：文件不存在：{path}"
        if file_path.is_dir():
            return f"错误：{path} 是一个目录，不是文件"
        return file_path.read_text(encoding="utf-8")

