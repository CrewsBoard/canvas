from flow_engine.flow_chain.dtos.input_types import InputTypes
from flow_engine.flow_chain.dtos.node_types import NodeTypes
from flow_engine.flow_chain.dtos.node_ui_config import NodeUiConfig, NodeUiFields
from flow_engine.flow_chain.dtos.output_types import OutputTypes

ui_config: NodeUiConfig = NodeUiConfig(
    is_start_node=True,
    type=NodeTypes.CREW,
    name="crewai_crew_node",
    title="CrewAI Crew Start Node",
    description="Start node for CrewAI",
    icon="ai",
    color="#9C27B0",
    inputs=[InputTypes.SUCCESS],
    outputs=[OutputTypes.SUCCESS],
    node_template_id="crewai_crew",
    fields=[
        NodeUiFields(
            label="Crew Node",
            description="This node is a CrewAI node",
        ),
    ],
)
