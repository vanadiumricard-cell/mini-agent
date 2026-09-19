from pathlib import Path
PROJECT_ROOT=Path(__file__).resolve().parents[3]
SKIP_DIRS={".venv",".git","__pycache__",".pytext_cache"}
def list_files(path:str=".",pattern:str="*")->str:
    dir_path=(PROJECT_ROOT/path).resolve()
    if not dir_path.is_relative_to(PROJECT_ROOT):
        return f"错误，访问项目目录之外的位置：{path}"
    if not dir_path.exists():
        return f"错误：目录不存在{path}"
    if not dir_path.is_dir():
        return f"错误：{path}不是目录"
    lines=[]
    for entry in sorted(dir_path.glob(pattern)):
        rel=entry.relative_to(PROJECT_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if entry.is_dir():
            lines.append(f"[目录]{rel}")
        else:
            lines.append(f"[文件]{rel}")
    if not lines:
        return "(没有匹配的文件或目录)"
    return"\n".join(lines)
list_files_schema={
    "type":"function",
    "function":{
        "name":"list_files",
        "description":"列出项目内某个目录的内容，pattern 支持通配符（如 *.py）；使用 **/*.py 可递归查找所有 Python 文件",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string",
                    "description":"目录路径（相对于项目根目录），默认为项目根目录",
                },
                "pattern": {
                    "type": "string",
                    "description": "文件名匹配模式（glob），默认为 *（列出所有）",
                },
            }
        }
    }
}

    
