from flow_engine.flow_chain.dtos import NodeTypes, OutputTypes, InputTypes, NodeUiConfig
from flow_engine.flow_chain.dtos.node_ui_config import NodeUiFields

ui_config: NodeUiConfig = NodeUiConfig(
    is_start_node=True,
    type=NodeTypes.CREW,
    name="crewai_crew_start_node",
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
