from tools import (get_time, calculator)
from logger import log_event

TOOL_REGISTRY = {

    "get_time":
        get_time,

    "calculator":
        calculator
}


def execute_tool(
    tool_name,
    arguments
):
    log_event(f"Tool Called: {tool_name}")
    log_event(f"Arguments: {arguments}")

    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {tool_name}")

    function = TOOL_REGISTRY[tool_name]

    try:
        return function(**arguments)
    except TypeError as error:
        raise ValueError(
            f"Invalid arguments for tool '{tool_name}': {error}"
        ) from error
    except Exception as error:
        raise RuntimeError(
            f"Tool '{tool_name}' failed: {error}"
        ) from error
