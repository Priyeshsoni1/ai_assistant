TIME_TOOL = {
    "type": "function",
    "function": {
        "name": "get_time",
        "description": "Get current system time",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}


CALCULATOR_TOOL = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Perform math operations",
        "parameters": {
            "type": "object",
            "properties": {

                "a": {
                    "type": "number"
                },

                "b": {
                    "type": "number"
                },

                "operation": {
                    "type": "string",
                    "enum": [
                        "+",
                        "-",
                        "*",
                        "/"
                    ]
                }
            },

            "required": [
                "a",
                "b",
                "operation"
            ]
        }
    }
}


TOOLS = [
    TIME_TOOL,
    CALCULATOR_TOOL
]