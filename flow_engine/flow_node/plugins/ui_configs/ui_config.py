NODE_UI_CONFIGS = {
    "input": {
        "title": "Input Node",
        "description": "Handles input messages and adds timestamps",
        "icon": "input",
        "color": "#4CAF50",
        "inputs": [],
        "outputs": ["Success"],
        "settings": {
            "add_timestamp": {
                "type": "boolean",
                "default": True,
                "label": "Add Timestamp",
            },
            "required_fields": {
                "type": "array",
                "default": ["data"],
                "label": "Required Fields",
            },
        },
    },
    "transform": {
        "title": "Transform Node",
        "description": "Transforms message data based on configuration",
        "icon": "transform",
        "color": "#2196F3",
        "inputs": ["Success"],
        "outputs": ["Success"],
        "settings": {
            "transformations": {
                "type": "object",
                "default": {},
                "label": "Transformations",
            }
        },
    },
    "output": {
        "title": "Output Node",
        "description": "Handles output messages and formatting",
        "icon": "output",
        "color": "#FF9800",
        "inputs": ["Success"],
        "outputs": [],
        "settings": {
            "format": {
                "type": "select",
                "options": ["json", "text"],
                "default": "json",
                "label": "Output Format",
            },
            "destination": {
                "type": "select",
                "options": ["console", "file"],
                "default": "console",
                "label": "Destination",
            },
        },
    },
}
