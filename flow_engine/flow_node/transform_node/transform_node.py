from typing import Dict, Any

from flow_engine.flow_chain.services import FlowNodeRegistry, FlowNode


@FlowNodeRegistry.register("transform")
class TransformNode(FlowNode):
    def __init__(self, name: str, configuration: Dict[str, Any] = None):
        super().__init__(name, "transform", configuration)

    def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply transformations to the message based on configuration.
        """
        result = message.copy()
        transformations = self.configuration.get("transformations", {})

        for field, transform_type in transformations.items():
            if field in result:
                if transform_type == "uppercase":
                    result[field] = str(result[field]).upper()
                elif transform_type == "increment":
                    if isinstance(result[field], (int, float)):
                        result[field] += 1
                elif transform_type == "reverse":
                    if isinstance(result[field], str):
                        result[field] = result[field][::-1]

        return result
