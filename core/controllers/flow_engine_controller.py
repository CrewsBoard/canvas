import importlib
import json
import os
import uuid
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException
from starlette.responses import StreamingResponse

from core.controllers.base_controller import BaseController
from flow_engine.flow_chain.dtos import (
    NodeUiConfig,
    FlowChain,
    NodeTypes,
)
from flow_engine.flow_chain.services import FlowNodeRegistry
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
            "/crewai/flow-chains",
            self.create_crewai_flow_chain,
            methods=["POST"],
            response_model=Dict[str, Any],
        )
        self.router.add_api_route(
            "/crewai/flow-chains/{chain_id}/execute",
            self.execute_crewai_flow_chain,
            methods=["POST"],
            response_model=Dict[str, Any],
        )

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

    async def create_crewai_flow_chain(self, request: Dict[str, Any]) -> Dict[str, Any]:
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
            self.flow_chains[flow_chain.id] = flow_chain
            nodes: List[Any] = []
            for node_request in flow_chain.nodes:
                node_class = FlowNodeRegistry.get_plugin(
                    request.get("node_template_id")
                )
                if not isinstance(node_request.configuration, dict):
                    node_request.configuration = node_request.configuration.model_dump()
                node = node_class(
                    flow_chain_id=flow_chain.id,
                    node_id=node_request.id,
                    name=node_request.name,
                    node_type=node_request.node_type,
                    configuration=node_request.configuration,
                    connections=flow_chain.connections,
                )
                nodes.append(node)
            self.flow_nodes[flow_chain.id] = nodes
            return {
                "flow_chain_id": flow_chain.id,
                "message": "CrewAI flow chain created successfully",
                "crew_created": True,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def execute_crewai_flow_chain(self, chain_id: str, request: Dict[str, Any]):
        try:
            flow_chain = self.flow_chains[chain_id]
            if not flow_chain:
                raise HTTPException(
                    status_code=404, detail="CrewAI flow chain not found"
                )
            first_node_id = flow_chain.first_node_id
            self.flow_chain_events[chain_id] = {}
            self.flow_chain_events[chain_id]["traversed_node"] = []
            self.flow_chain_events[chain_id]["traversed_node"].append(first_node_id)
            flow_nodes = self.flow_nodes.get(flow_chain.id)
            total_tool_nodes = len(
                [
                    node
                    for node in flow_nodes
                    if node.type == NodeTypes.TOOL or node.type == NodeTypes.CREW
                ]
            )

            async def stream_data():
                last_index = 0
                user_msg = request
                has_init = False
                while True:
                    if not has_init:
                        self.event.set()
                        has_init = True
                    await self.event.wait()
                    self.event.clear()

                    while last_index <= total_tool_nodes - 1:
                        traversed_node = self.flow_chain_events.get(flow_chain.id).get(
                            "traversed_node"
                        )
                        if len(traversed_node) == last_index:
                            yield json.dumps(
                                {
                                    "flow_chain_id": chain_id,
                                    "message": "Flow chain completed",
                                }
                            ).encode("utf-8")
                            return
                        flow_node_id = traversed_node[last_index]
                        all_msg = self.flow_chain_events.get(flow_chain.id).get(
                            "message"
                        )
                        node_msg = None
                        if all_msg:
                            node_msg = all_msg.get(flow_node_id)
                        message = node_msg if node_msg else user_msg

                        flow_node = next(
                            (node for node in flow_nodes if node.id == flow_node_id),
                            None,
                        )
                        flow_node.process(message)
                        last_index += 1
                        yield json.dumps(
                            self.flow_chain_events.get(flow_chain.id)
                        ).encode("utf-8")
                        if last_index == len(flow_chain.nodes) - 1:
                            yield json.dumps(
                                {"flow_chain_id": chain_id, "result": message}
                            ).encode("utf-8")

            return StreamingResponse(stream_data(), media_type="text/event-stream")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
