from typing import Dict, Any, Optional

from flow_engine.flow_chain.dtos import FlowNodeConfigs
from flow_engine.flow_chain.services import FlowNodeRegistry
from flow_engine.flow_chain.services.flow_node import FlowNode


@FlowNodeRegistry.register("transform")
class TransformNode(FlowNode):
    def __init__(self, config: FlowNodeConfigs):
        super().__init__(config)

    async def process(self, message: Optional[Dict[str, Any]] = None) -> None:
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

        await self.next(result)
