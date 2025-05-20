from flow_engine.flow_chain.dtos.input_types import InputTypes
from flow_engine.flow_chain.dtos.node_types import NodeTypes
from flow_engine.flow_chain.dtos.node_ui_config import NodeUiConfig, NodeUiFields

ui_config: NodeUiConfig = NodeUiConfig(
    type=NodeTypes.TOOL,
    name="output_node",
    title="Output Node",
    description="Handles output messages and formatting",
    icon="output",
    color="#FF9800",
    inputs=[InputTypes.SUCCESS],
    outputs=[],
    node_template_id="output",
    fields=[
        NodeUiFields(
            label="Output Data",
            description="The data to be output from the node",
        ),
    ],
)
