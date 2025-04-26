import asyncio
from typing import Any, Dict, Optional, List

from pydantic import UUID4

from core.dtos.flow_engine import FlowEngineEventFactory
from flow_engine.flow_chain.dtos import FlowChain, FlowNodeConfigs, NodeTypes
from shared.services.msg_broker import AbstractMessageBroker


class FlowEngineService:
    _unique_flow_chain_identifier_placeholder = "_flow_engine_{}_"

    # @todo it will be deprecated after msg broker integration
    event = asyncio.Event()

    # @todo this dict needs to be cleared after user session ends
    flow_engine_node_factory: Dict[UUID4, Dict[NodeTypes, Dict[str, Any]]] = {}
    # @todo this dict needs to be cleared after a flow chain execution completes
    flow_engine_event_factory: Dict[UUID4, FlowEngineEventFactory] = {}
    flow_engine_agent_factory: Dict[str, List[Any]] = {}

    def __init__(self, caching_service: AbstractMessageBroker):
        self._caching_service = caching_service

    async def _create_flow_nodes(self, flow_chain: FlowChain) -> None:
        from flow_engine.flow_chain.services import FlowNodeRegistry

        self.flow_engine_node_factory[flow_chain.id] = {}
        for node_request in flow_chain.nodes:
            node_class = FlowNodeRegistry.get_plugin(node_request.node_template_id)
            if not isinstance(node_request.configuration, dict):
                node_request.configuration = node_request.configuration.model_dump()
            params = FlowNodeConfigs(
                flow_chain_id=flow_chain.id,
                node_id=node_request.id,
                name=node_request.name,
                node_type=node_request.node_type,
                configuration=node_request.configuration,
                connections=flow_chain.connections,
            )
            node = node_class(params)
            if not self.flow_engine_node_factory[flow_chain.id].get(params.node_type):
                self.flow_engine_node_factory[flow_chain.id][params.node_type] = {}
            self.flow_engine_node_factory[flow_chain.id][params.node_type][
                params.node_id
            ] = {}
            self.flow_engine_node_factory[flow_chain.id][params.node_type][
                params.node_id
            ] = node
            if params.node_type is NodeTypes.AGENT:
                await node.process()

    async def save_flow_chain(self, flow_chain: FlowChain):
        key = self._unique_flow_chain_identifier_placeholder.format(flow_chain.id)
        await self._create_flow_nodes(flow_chain)
        # @todo need to integrate save flow chain to db
        return await self._caching_service.set(key, flow_chain)

    async def read_flow_chains(
        self, flow_chain_id: Optional[UUID4] = None
    ) -> List[FlowChain]:
        flow_chains = []
        if not flow_chain_id:
            key = self._unique_flow_chain_identifier_placeholder.format("*")
            # @todo here need to integrate cache miss service from db
            flow_chain_data = await self._caching_service.get_all(key)
            for data in flow_chain_data:
                flow_chains.append(FlowChain.model_validate(flow_chain_data[data]))
        else:
            key = self._unique_flow_chain_identifier_placeholder.format(flow_chain_id)
            # @todo here need to integrate cache miss service from db
            flow_chain_data = await self._caching_service.get(key)
            flow_chains.append(FlowChain.model_validate(flow_chain_data))
        if not len(flow_chains):
            raise ValueError(f"Flow chain with ID {flow_chain_id} not found.")
        return flow_chains

    async def get_flow_nodes(self, flow_chain: FlowChain) -> Dict[str, Any]:
        flow_nodes = self.flow_engine_node_factory.get(flow_chain.id, {})
        if not flow_nodes:
            await self._create_flow_nodes(flow_chain)
        return self.flow_engine_node_factory.get(flow_chain.id)

    def total_none_agent_node(self, flow_chain_id: UUID4) -> int:
        total_tool_nodes = 0
        flow_nodes = self.flow_engine_node_factory.get(str(flow_chain_id), {})
        for node_type in flow_nodes:
            if node_type is not NodeTypes.AGENT:
                total_tool_nodes += len(flow_nodes[node_type])
        return total_tool_nodes

    def get_agent_nodes(self, flow_chain_id: UUID4) -> List[Any]:
        agents = []
        flow_nodes: Dict[NodeTypes, Dict[str, Any]] = self.flow_engine_node_factory.get(
            str(flow_chain_id), {}
        )
        for node_type in flow_nodes:
            if node_type is NodeTypes.AGENT:
                agents.extend([value for value in flow_nodes[node_type].values()])
        return agents
