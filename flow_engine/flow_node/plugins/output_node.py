from typing import Dict, Any

from flow_engine.flow_chain.services.plugin_base import FlowNode
from flow_engine.flow_chain.services.plugin_registry import PluginRegistry


@PluginRegistry.register("output")
class OutputNode(FlowNode):
    def __init__(self, name: str, configuration: Dict[str, Any] = None):
        super().__init__(name, "output", configuration)

    def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the output message based on configuration.
        """
        output_format = self.configuration.get("format", "json")
        destination = self.configuration.get("destination", "console")

        if destination == "console":
            if output_format == "json":
                print("Output:", message)
            elif output_format == "text":
                print("Output:", str(message))

        return message
