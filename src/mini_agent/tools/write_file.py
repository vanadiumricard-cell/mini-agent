from pathlib import Path
from mini_agent.tools.base import Tool

PROJECT_ROOT =Path(__file__).resolve().parents[3]
class WriteFileTool(Tool):
    name = "write_file"
    description = "在项目内创建或覆盖一个文本文件（执行前会请求用户确认）"
    parameters = {
        "path": {
            "type": "string",
            "description": "文件路径（相对于项目根目录，例如 sandbox/note.txt）",
        },
        "content": {
            "type": "string",
            "description": "要写入的完整文件内容",
        },
    }
    required = ["path", "content"]

    def run(self, path, content):
        file_path = (PROJECT_ROOT / path).resolve()
        if not file_path.is_relative_to(PROJECT_ROOT):
            return f"错误：拒绝写入项目目录之外的位置：{path}"
        if file_path.is_dir():
            return f"错误：{path} 是一个目录"

        action = "覆盖" if file_path.exists() else "新建"
        print(f"\n[写入请求] {action}文件: {path}（{len(content)} 字符）")
        answer = input("允许写入吗？(y/n): ")
        if answer != "y":
            return "错误：用户拒绝了本次写入"

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"写入成功：{path}（{len(content)} 字符）"
