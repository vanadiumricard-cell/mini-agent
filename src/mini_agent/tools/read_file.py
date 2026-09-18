from pathlib import Path
PROJECT_ROOT=Path(__file__).resolve().parents[3]
def read_file(path:str)->str:
    file_path=(PROJECT_ROOT/path).resolve()
    if not file_path.is_relative_to(PROJECT_ROOT):
        return f"错误：访问错误路径{path}"
    if not file_path.exists():
        return f"错误：文件不存在{path}"
    if file_path.is_dir():
        return f"错误：{path}是文件夹"
    return file_path.read_text(encoding="utf-8")
read_file_schema={
    "type":"function",
     "function": {
        "name": "read_file",
        "description": "读取项目内的一个文本文件并返回其内容",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "文件路径（相对于项目根目录，例如 src/mini_agent/agent.py）",
                },
            },
            "required": ["path"],
        },
    },
}

