import importlib
import os
import uuid
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import UUID4

from core.controllers.base_controller import BaseController
from core.dtos.flow_engine import (
    FlowEngineExecuteParams,
)
from flow_engine.flow_chain.dtos import (
    NodeUiConfig,
    FlowChain,
)
from shared.dtos.msg_broker import FlowEngineMsg
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
            "/flow-chain",
            self.create_or_update_flow_chain,
            methods=["POST"],
            response_model=Dict[str, Any],
        )
        self.router.add_api_route(
            "/flow-chains",
            self.read_flow_chains,
            methods=["GET"],
            response_model=List[FlowChain],
        )
        self.router.add_api_route(
            "/flow-chain/execute",
            self.execute_flow_chain,
            methods=["POST"],
            response_model=Dict[str, Any],
        )

    # @todo this should be connected to db
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

    async def create_or_update_flow_chain(
        self, request: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            flow_chain = FlowChain(
                id=uuid.uuid4(),
                name=request.get("name", "Unnamed CrewAI Flow"),
                description=request.get("description"),
                nodes=request.get("nodes", []),
                connections=request.get("connections", []),
                debug_mode=request.get("debug_mode", False),
                first_node_id=request.get("first_node_id"),
            )
            await self.flow_engine_service.save_flow_chain(flow_chain)
            return {
                "flow_chain_id": flow_chain.id,
                "message": "CrewAI flow chain created successfully",
                "crew_created": True,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def read_flow_chains(
        self, flow_chain_id: Optional[UUID4] = None
    ) -> List[FlowChain]:
        return await self.flow_engine_service.read_flow_chains(flow_chain_id)

    async def execute_flow_chain(
        self, flow_engine_execute_params: FlowEngineExecuteParams
    ):
        try:
            message = FlowEngineMsg(
                flow_chain_id=flow_engine_execute_params.flow_chain_id,
                data=flow_engine_execute_params.data,
                node_id=flow_engine_execute_params.start_node_id,
                start_node_id=flow_engine_execute_params.start_node_id,
            )
            is_executed = await self.flow_engine_service.next(
                flow_chain_id=flow_engine_execute_params.flow_chain_id,
                next_msg=message,
            )
            return {
                "flow_chain_id": str(flow_engine_execute_params.flow_chain_id),
                "message": "Flow chain executed successfully",
                "result": is_executed,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
