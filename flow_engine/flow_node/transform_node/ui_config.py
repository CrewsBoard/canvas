from flow_engine.flow_chain.dtos import NodeTypes, OutputTypes, InputTypes, NodeUiConfig
from flow_engine.flow_chain.dtos.node_ui_config import NodeUiFields

ui_config: NodeUiConfig = NodeUiConfig(
    type=NodeTypes.TOOL,
    name="transform_node",
    title="Transform Node",
    description="Transforms message data based on configuration",
    icon="transform",
    color="#2196F3",
    inputs=[InputTypes.SUCCESS],
    outputs=[OutputTypes.SUCCESS, OutputTypes.FAILURE],
    node_template_id="transform",
    fields=[
        NodeUiFields(
            label="Transformations",
            description="The transformations to be applied to the data",
        ),
    ],
)
