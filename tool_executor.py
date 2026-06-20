from tools import (get_time, calculator)

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

    function = TOOL_REGISTRY[
        tool_name
    ]

    return function(
        **arguments
    )