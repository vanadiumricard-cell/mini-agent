from datetime import datetime
from mini_agent.tools.base import Tool


class CurrentTimeTool(Tool):
    name = "get_current_time"
    description = "获得当前的日期和时间"

    def run(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
