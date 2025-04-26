from typing import Dict, Any, Optional

from flow_engine.flow_chain.dtos import FlowNodeConfigs
from flow_engine.flow_chain.services import FlowNodeRegistry
from flow_engine.flow_chain.services.flow_node import FlowNode


@FlowNodeRegistry.register("output")
class OutputNode(FlowNode):
    def __init__(self, config: FlowNodeConfigs):
        super().__init__(config)

    async def process(self, message: Optional[Dict[str, Any]] = None) -> None:
        await self.next(message)
