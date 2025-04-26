import importlib
import json
import os
import uuid
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from starlette.responses import StreamingResponse

from core.controllers.base_controller import BaseController
from core.dtos.flow_engine import FlowEngineEventFactory
from flow_engine.flow_chain.dtos import (
    NodeUiConfig,
    FlowChain,
    NodeTypes,
)
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
            "/flow-chain/{flow_chain_id}/execute",
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
                id=str(uuid.uuid4()),
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

    async def execute_flow_chain(self, flow_chain_id: UUID4, request: Dict[str, Any]):
        try:
            flow_chains = await self.flow_engine_service.read_flow_chains(flow_chain_id)
            flow_chain = flow_chains[0]
            if not flow_chain:
                raise HTTPException(
                    status_code=404, detail="CrewAI flow chain not found"
                )
            first_node_id = flow_chain.first_node_id
            self.flow_engine_service.flow_engine_event_factory[
                flow_chain_id
            ] = FlowEngineEventFactory()
            self.flow_engine_service.flow_engine_event_factory[
                flow_chain_id
            ].traversed_node.append(first_node_id)
            flow_nodes = await self.flow_engine_service.get_flow_nodes(flow_chain)
            total_tool_nodes = self.flow_engine_service.total_none_agent_node(
                flow_chain_id
            )

            async def stream_data():
                last_index = 0
                user_msg = request
                has_init = False
                while True:
                    if not has_init:
                        self.flow_engine_service.event.set()
                        has_init = True
                    await self.flow_engine_service.event.wait()
                    self.flow_engine_service.event.clear()

                    while last_index <= total_tool_nodes - 1:
                        traversed_node = (
                            self.flow_engine_service.flow_engine_event_factory.get(
                                flow_chain_id
                            ).traversed_node
                        )
                        if len(traversed_node) == last_index:
                            yield json.dumps(
                                {
                                    "flow_chain_id": str(flow_chain_id),
                                    "message": "Flow chain completed",
                                }
                            ).encode("utf-8")
                            return
                        flow_node_id = traversed_node[last_index]
                        all_msg = (
                            self.flow_engine_service.flow_engine_event_factory.get(
                                flow_chain_id
                            ).message
                        )
                        node_msg = all_msg.get(flow_node_id) if all_msg else None
                        message = node_msg if node_msg else user_msg

                        flow_node = next(
                            (
                                flow_nodes[node_type][flow_node_id]
                                for node_type in flow_nodes
                                if node_type is not NodeTypes.AGENT
                                and flow_nodes.get(node_type).get(flow_node_id)
                                is not None
                            ),
                            None,
                        )
                        await flow_node.process(message)
                        last_index += 1
                        yield json.dumps(
                            self.flow_engine_service.flow_engine_event_factory.get(
                                flow_chain_id
                            ).model_dump()
                        ).encode("utf-8")
                        if last_index == len(flow_chain.nodes) - 1:
                            yield json.dumps(
                                {"flow_chain_id": str(flow_chain_id), "result": message}
                            ).encode("utf-8")

            return StreamingResponse(stream_data(), media_type="text/event-stream")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
