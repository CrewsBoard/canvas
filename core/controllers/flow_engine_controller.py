import uuid
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException

from core.controllers.base_controller import BaseController
from flow_engine.flow_chain.dtos.flow_engine import (
    FlowChainRequest,
    MessageRequest,
    NodeTypeResponse,
    FlowChainResponse,
)
from flow_engine.flow_chain.models.flow_chain import NodeConnection, FlowChain
from flow_engine.flow_chain.services.plugin_registry import PluginRegistry
from flow_engine.flow_node.plugins.ui_configs import NODE_UI_CONFIGS


class FlowEngineController(BaseController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(tags=self.flow_engine_swagger_tags)

        self.router.add_api_route(
            "/node-types",
            self.get_node_types,
            methods=["GET"],
            response_model=List[NodeTypeResponse],
        )
        self.router.add_api_route(
            "/flow-chains",
            self.create_flow_chain,
            methods=["POST"],
            response_model=FlowChainResponse,
        )
        self.router.add_api_route(
            "/flow-chains/{chain_id}",
            self.get_flow_chain,
            methods=["GET"],
            response_model=FlowChainResponse,
        )
        self.router.add_api_route(
            "/flow-chains/{chain_id}/process",
            self.process_message,
            methods=["POST"],
            response_model=Dict[str, Any],
        )

        self.flow_chains: Dict[str, FlowChain] = {}

    @staticmethod
    async def get_node_types() -> List[NodeTypeResponse]:
        node_types = []
        for node_type, config in NODE_UI_CONFIGS.items():
            node_types.append(
                NodeTypeResponse(
                    type=node_type,
                    title=config["title"],
                    description=config["description"],
                    icon=config["icon"],
                    color=config["color"],
                    inputs=config["inputs"],
                    outputs=config["outputs"],
                    settings=config["settings"],
                )
            )
        return node_types

    async def create_flow_chain(self, request: FlowChainRequest) -> FlowChainResponse:
        try:
            nodes = []
            node_name_to_id = {}
            for node_request in request.nodes:
                node_class = PluginRegistry.get_plugin(node_request.type)
                node = node_class(
                    name=node_request.name, configuration=node_request.configuration
                )
                nodes.append(node)
                node_name_to_id[node_request.name] = node.id

            connections = [
                NodeConnection(
                    from_node_id=node_name_to_id[conn.from_node],
                    to_node_id=node_name_to_id[conn.to_node],
                    label=conn.type,
                )
                for conn in request.connections
            ]

            chain_id = str(uuid.uuid4())
            flow_chain = FlowChain(
                id=chain_id,
                name=request.name,
                nodes=nodes,
                connections=connections,
                first_node_id=node_name_to_id.get(request.first_node_id),
                debug_mode=request.debug_mode,
            )

            self.flow_chains[chain_id] = flow_chain

            return FlowChainResponse(
                id=chain_id,
                name=request.name,
                status="created",
                message="Flow chain created successfully",
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_flow_chain(self, chain_id: str) -> FlowChainResponse:
        if chain_id not in self.flow_chains:
            raise HTTPException(status_code=404, detail="Flow chain not found")

        chain = self.flow_chains[chain_id]
        return FlowChainResponse(
            id=chain.id,
            name=chain.name,
            status="active",
            message="Flow chain retrieved successfully",
        )

    async def process_message(
        self, chain_id: str, message: MessageRequest
    ) -> Dict[str, Any]:
        if chain_id not in self.flow_chains:
            raise HTTPException(status_code=404, detail="Flow chain not found")

        try:
            result = self.flow_chains[chain_id].process_message(
                {"data": message.dict()}
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
