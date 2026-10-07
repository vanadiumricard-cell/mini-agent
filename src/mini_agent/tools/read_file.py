from pathlib import Path
from mini_agent.tools.base import Tool
PROJECT_ROOT=Path(__file__).resolve().parents[3]
class ReadFileTool(Tool):
    name = "read_file"
    description = "读取项目内的一个文本文件并返回其内容，\
    单次最多返回 200 行；文件较长时可用 start_line 指定起始行继续读取（行号从 1 开始）"
    parameters = {
        "path": {
            "type": "string",
            "description": "文件路径（相对于项目根目录，例如 src/mini_agent/agent.py）",
        },
        "start_line":{
            "type":"integer",
            "description":"起始行号，默认为1"
        },
        "end_line":{
            "type":"integer",
            "description":"结束行号(可选)，单次最多读取200行"
        },
    }
    required = ["path"]
    MAX_LINES = 200
    def run(self, path,start_line=1,end_line=None):
        file_path = (PROJECT_ROOT / path).resolve()
        if not file_path.is_relative_to(PROJECT_ROOT):
            return f"错误：拒绝访问项目目录之外的文件：{path}"
        if not file_path.exists():
            return f"错误：文件不存在：{path}"
        if file_path.is_dir():
            return f"错误：{path} 是一个目录，不是文件"
        lines= file_path.read_text(encoding="utf-8").splitlines()
        total=len(lines)
        if total==0:
            return f"[文件{path}|空文件]"
        start =max(1,start_line)
        if start > total:
            return f"错误：起始行 {start} 超过文件总行数（共 {total} 行）"
        if end_line is None:
            end = start + self.MAX_LINES - 1
        else:
            end = min(end_line, start + self.MAX_LINES - 1)
        end=min(end,total)
        if start>end:
             return f"错误：行号范围无效：start_line={start}, end_line={end_line}"
        body="\n".join(lines[start-1:end])
        header = f"[文件 {path} | 共 {total} 行 | 显示第 {start}-{end} 行]"
        if end < total:
            body += f"\n...（还有 {total - end} 行未显示，可用 start_line={end + 1} 继续读取）"
        return header + "\n" + body
