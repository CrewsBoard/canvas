from datetime import datetime
from typing import Dict, Any

from flow_engine.flow_chain.services.plugin_base import FlowNode
from flow_engine.flow_chain.services.plugin_registry import PluginRegistry


@PluginRegistry.register("input")
class InputNode(FlowNode):
    def __init__(self, name: str, configuration: Dict[str, Any] = None):
        super().__init__(name, "input", configuration)

    def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input message and add timestamp if configured.
        """
        message_data = message.copy().get("data").get("data")

        if self.configuration.get("add_timestamp", False):
            message_data["timestamp"] = datetime.utcnow().isoformat()

        required_fields = self.configuration.get("required_fields", [])
        for field in required_fields:
            if field not in message_data:
                raise ValueError(f"Required field '{field}' not found in message")

        return message_data
