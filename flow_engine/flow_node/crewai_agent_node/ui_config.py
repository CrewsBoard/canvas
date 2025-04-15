from flow_engine.flow_chain.dtos import NodeTypes, OutputTypes, InputTypes, NodeUiConfig
from flow_engine.flow_chain.dtos.node_ui_config import NodeUiFields

ui_config: NodeUiConfig = NodeUiConfig(
    type=NodeTypes.AGENT,
    name="crewai_agent_node",
    title="CrewAI Agent",
    description="An AI agent that can perform tasks using CrewAI",
    icon="ai",
    color="#9C27B0",
    inputs=[InputTypes.SUCCESS],
    outputs=[OutputTypes.SUCCESS],
    fields=[
        NodeUiFields(
            label="Agent Role",
            description="Agent Role",
            type="str",
            default="",
            required=True,
        ),
        NodeUiFields(
            label="Agent Goal",
            description="Agent Goal",
            type="str",
            default="",
            required=True,
        ),
        NodeUiFields(
            label="Agent Backstory",
            description="Agent Backstory",
            type="str",
            default="",
            required=True,
        ),
        NodeUiFields(
            label="Agent Tools",
            description="Agent Tools",
            type="list[str]",
            default=[],
            required=False,
        ),
    ],
)
