import json

from crewai.tools import tool


@tool("Prepare input for TransformNode")
def prepare_transform_node_input(message_json: str, transformations_json: str) -> str:
    """
    Prepares input and configuration for the TransformNode.

    Parameters:
    - message_json: A JSON string representing the message dictionary. Example: '{"name": "john", "age": 30}'
    - transformations_json: A JSON string mapping fields to transformation types. Example: '{"name": "uppercase", "age": "increment"}'

    Returns:
    - A JSON string containing the properly formatted input for the TransformNode
    """
    try:
        message = json.loads(message_json)
        transformations = json.loads(transformations_json)
    except json.JSONDecodeError as e:
        return f"Invalid JSON input: {e}"

    prepared_input = {
        "message": message,
        "configuration": {"transformations": transformations},
    }

    return json.dumps(prepared_input, indent=2)
