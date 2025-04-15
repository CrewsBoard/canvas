from flow_engine.flow_chain.dtos import NodeTypes, OutputTypes, NodeUiConfig
from flow_engine.flow_chain.dtos.node_ui_config import NodeUiFields

ui_config: NodeUiConfig = NodeUiConfig(
    type=NodeTypes.TOOL,
    name="input_node",
    title="Input Node",
    description="Handles input messages and adds timestamps",
    icon="input",
    color="#4CAF50",
    inputs=[],
    outputs=[OutputTypes.SUCCESS],
    node_template_id="input",
    fields=[
        NodeUiFields(
            label="Input Data",
            description="The data to be input into the node",
            type="str",
            default="",
            required=True,
        ),
    ],
)
