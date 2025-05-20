from typing import Any, Dict, Optional

from flow_engine.flow_chain.dtos.flow_node_configs import FlowNodeConfigs
from flow_engine.flow_chain.services.flow_node import FlowNode
from flow_engine.flow_chain.services.flow_node_registry_service import FlowNodeRegistry


@FlowNodeRegistry.register("output")
class OutputNode(FlowNode):
    def __init__(self, config: FlowNodeConfigs):
        super().__init__(config)

    async def process(self, message: Optional[Dict[str, Any]] = None) -> None:
        await self.next(message)
