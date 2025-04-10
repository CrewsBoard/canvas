import importlib
import os
import uuid
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException

from core.controllers.base_controller import BaseController
from flow_engine.flow_chain.dtos import NodeConnection, NodeUiConfig
from flow_engine.flow_chain.dtos.flow_engine import (
    FlowChainRequest,
    MessageRequest,
    FlowChainResponse,
)
from flow_engine.flow_chain.services import FlowNodeRegistry
from flow_engine.flow_chain.services.flow_chain_service import FlowChainService
from shared.utils.funcs import get_root_path


class FlowEngineController(BaseController):
    def __init__(self):
        super().__init__()
        self.router = APIRouter(tags=self.flow_engine_swagger_tags)

        self.router.add_api_route(
            "/node-types",
            self.get_node_types,
            methods=["GET"],
            response_model=List[NodeUiConfig],
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

        self.flow_chains: Dict[str, FlowChainService] = {}

    @staticmethod
    async def get_node_types() -> List[NodeUiConfig]:
        node_types = []
        root_path = get_root_path()
        flow_nodes_path = os.path.join(root_path, "flow_engine", "flow_node")
        node_ui_configs: List[NodeUiConfig] = []
        for root, dirs, files in os.walk(flow_nodes_path):
            if "ui_config.py" in files:
                ui_config_path = os.path.join(root, "ui_config.py")
                try:
                    spec = importlib.util.spec_from_file_location(
                        "ui_config", ui_config_path
                    )
                    ui_config_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(ui_config_module)
                    if hasattr(ui_config_module, "ui_config"):
                        node_ui_configs.append(ui_config_module.ui_config)
                except Exception as e:
                    print(f"Error loading {ui_config_path}: {e}")
        return node_ui_configs

    async def create_flow_chain(self, request: FlowChainRequest) -> FlowChainResponse:
        try:
            nodes = []
            node_name_to_id = {}
            for node_request in request.nodes:
                node_class = FlowNodeRegistry.get_plugin(node_request.type)
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
            flow_chain = FlowChainService(
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
