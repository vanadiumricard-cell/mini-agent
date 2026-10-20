import sys
from pathlib import Path

from mini_agent.mcp import MCPClient, MCPConnectionError
from mini_agent.mcp.remote_tool import register_mcp_tools
from mini_agent.tools import CalculatorTool, ToolRegistry

ROOT = Path(__file__).resolve().parents[1]
SERVER = [sys.executable, str(ROOT / "mcp_servers" / "calculator_server.py")]


def make_client():
    client = MCPClient(SERVER)
    client.start()
    client.initialize()
    return client


def test_tools_list_and_call():
    client = make_client()
    try:
        names = [t["name"] for t in client.list_tools()]
        assert "calculator" in names
        assert "roll_dice" in names

        result = client.call_tool("calculator", {"a": 123, "b": 456, "operation": "multiply"})
        assert result["content"][0]["text"] == "56088"
    finally:
        client.close()


def test_adapter_roundtrip_schema():
    client = make_client()
    try:
        registry = ToolRegistry()
        register_mcp_tools(registry, client)
        assert registry.get_schemas()[0] == CalculatorTool().to_schema()
    finally:
        client.close()


def test_business_error_is_data():
    client = make_client()
    try:
        result = client.call_tool("calculator", {"a": 5, "b": 0, "operation": "divide"})
        assert result["isError"] is True
        assert "除数不能为零" in result["content"][0]["text"]
    finally:
        client.close()


def test_connection_error_and_restart():
    client = make_client()
    try:
        client.process.kill()
        client.process.wait()
        try:
            client.call_tool("calculator", {"a": 1, "b": 1, "operation": "add"})
            assert False, "应该抛出 MCPConnectionError"
        except MCPConnectionError:
            pass

        client.restart()
        result = client.call_tool("calculator", {"a": 1, "b": 1, "operation": "add"})
        assert result["content"][0]["text"] == "2"
    finally:
        client.close()