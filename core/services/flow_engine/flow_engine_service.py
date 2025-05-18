import asyncio
from typing import Any, Dict, Optional, List

from fastapi import HTTPException
from pydantic import UUID4

from flow_engine.flow_chain.dtos import FlowChain, FlowNodeConfigs, NodeTypes
from shared.dtos.msg_broker import FlowEngineMsg
from shared.services.msg_broker import AbstractMessageBroker
from shared.utils.logger import logger


class FlowEngineService:
    UNIQUE_FLOW_CHAIN_IDENTIFIER_PLACEHOLDER = "_flow_engine_{}_"

    # @todo this dict needs to be cleared after user session ends
    flow_engine_node_factory: Dict[UUID4, Dict[NodeTypes, Dict[str, Any]]] = {}
    flow_engine_agent_factory: Dict[UUID4, List[Any]] = {}
    history = []

    def __init__(
        self,
        msg_broker_service: AbstractMessageBroker,
        caching_service: AbstractMessageBroker,
    ):
        self.msg_broker_service = msg_broker_service
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
            self.flow_engine_node_factory[flow_chain.id][params.node_type][params.node_id] = {}
            self.flow_engine_node_factory[flow_chain.id][params.node_type][params.node_id] = node
            if params.node_type is NodeTypes.AGENT:
                await node.process()

    async def _flow_engine_event_handler(
        self,
        flow_engine_msg: Dict[str, Any],
    ) -> None:
        logger.info(f"Flow engine event handler: {flow_engine_msg}")
        flow_engine_msg = FlowEngineMsg.model_validate(flow_engine_msg)
        flow_chains = await self.read_flow_chains(flow_engine_msg.flow_chain_id)
        flow_chain = flow_chains[0]
        if not flow_chain:
            raise HTTPException(status_code=404, detail="CrewAI flow chain not found")
        flow_nodes = await self.get_flow_nodes(flow_chain)
        flow_node_id = flow_engine_msg.node_id
        flow_node = next(
            (
                flow_nodes[node_type][flow_node_id]
                for node_type in flow_nodes
                if node_type is not NodeTypes.AGENT and flow_nodes.get(node_type).get(flow_node_id) is not None
            ),
            None,
        )
        await flow_node(flow_engine_msg)

        # @todo this portion will be removed
        self.history.append(flow_engine_msg)

    async def next(self, flow_chain_id: UUID4, next_msg: FlowEngineMsg) -> bool:
        try:
            key = self.UNIQUE_FLOW_CHAIN_IDENTIFIER_PLACEHOLDER.format(str(flow_chain_id))
            has_subscription = await self.msg_broker_service.check_subscription(key)
            if not has_subscription:
                await self.msg_broker_service.subscribe(key, self._flow_engine_event_handler)
            asyncio.create_task(self.msg_broker_service.publish(key, next_msg.model_dump()))
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            return False
        return True

    async def save_flow_chain(self, flow_chain: FlowChain):
        key = self.UNIQUE_FLOW_CHAIN_IDENTIFIER_PLACEHOLDER.format(flow_chain.id)
        await self._create_flow_nodes(flow_chain)
        await self.msg_broker_service.subscribe(key, self._flow_engine_event_handler)
        # @todo need to integrate save flow chain to db
        return await self._caching_service.set(key, flow_chain)

    async def read_flow_chains(self, flow_chain_id: Optional[UUID4] = None) -> List[FlowChain]:
        flow_chains = []
        if not flow_chain_id:
            key = self.UNIQUE_FLOW_CHAIN_IDENTIFIER_PLACEHOLDER.format("*")
            # @todo here need to integrate cache miss service from db
            flow_chain_data = await self._caching_service.get_all(key)
            for data in flow_chain_data:
                flow_chains.append(FlowChain.model_validate(flow_chain_data[data]))
        else:
            key = self.UNIQUE_FLOW_CHAIN_IDENTIFIER_PLACEHOLDER.format(flow_chain_id)
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
        flow_nodes: Dict[NodeTypes, Dict[str, Any]] = self.flow_engine_node_factory.get(str(flow_chain_id), {})
        for node_type in flow_nodes:
            if node_type is NodeTypes.AGENT:
                agents.extend([value for value in flow_nodes[node_type].values()])
        return agents
