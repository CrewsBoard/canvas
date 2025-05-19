from flow_engine.flow_chain.dtos.input_types import InputTypes
from flow_engine.flow_chain.dtos.node_types import NodeTypes
from flow_engine.flow_chain.dtos.node_ui_config import NodeUiConfig, NodeUiFields

# @todo remove after all the integration of dynamic nodes is done
ui_config: NodeUiConfig = NodeUiConfig(
    type=NodeTypes.TOOL,
    name="my_custom_node",
    title="My Custom Node",
    description="A custom node implementation",
    icon="custom",
    color="#FF5722",
    inputs=[InputTypes.SUCCESS],
    outputs=[],
    node_template_id="my_custom_node",
    fields=[
        NodeUiFields(
            label="Custom Field",
            description="The data to be output from the node",
        ),
    ],
    ui_bundle="http://localhost:3002/canvas-custom-node.es.js",
)
