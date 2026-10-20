import pytest

from mini_agent.tools import CalculatorTool, Tool, ToolRegistry


def test_calculator_operations():
    tool = CalculatorTool()
    assert tool.run(2, 3, "add") == 5
    assert tool.run(10, 4, "subtract") == 6
    assert tool.run(6, 7, "multiply") == 42
    assert tool.run(9, 3, "divide") == 3


def test_calculator_divide_by_zero():
    with pytest.raises(ValueError):
        CalculatorTool().run(1, 0, "divide")


def test_schema_shape():
    schema = CalculatorTool().to_schema()
    assert schema["type"] == "function"
    function = schema["function"]
    assert function["name"] == "calculator"
    assert set(function["parameters"]["properties"]) == {"a", "b", "operation"}
    assert function["parameters"]["required"] == ["a", "b", "operation"]


def test_registry_register_and_get():
    registry = ToolRegistry()
    tool = CalculatorTool()
    registry.register(tool)
    assert registry.get("calculator") is tool
    assert registry.get("nope") is None
    assert registry.get_schemas()[0]["function"]["name"] == "calculator"


def test_validate_rejects_typo_key():
    class BadTool(Tool):
        name = "bad"
        description = "坏工具"
        parameters = {"x": {"type": "string", "dsecription": "拼错的键"}}
        required = ["x"]

    with pytest.raises(ValueError):
        ToolRegistry().register(BadTool())