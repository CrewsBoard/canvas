import importlib
import os
from typing import Dict, Type

from flow_engine.flow_chain.services.flow_node import FlowNode
from shared.utils import logger
from shared.utils.funcs import get_root_path


class FlowNodeRegistry:
    _instance = None
    _plugins: Dict[str, Type[FlowNode]] = {}
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FlowNodeRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls) -> None:
        if not cls._initialized:
            logger.info("Initializing FlowNodeRegistry...")
            cls._load_all_plugins()
            cls._initialized = True
            logger.info(
                f"FlowNodeRegistry initialized with plugins: {list(cls._plugins.keys())}"
            )

    @classmethod
    def _load_all_plugins(cls) -> None:
        flow_nodes_path = os.path.join(get_root_path(), "flow_engine", "flow_node")
        logger.info(f"Loading plugins from: {flow_nodes_path}")

        for node_dir in os.listdir(flow_nodes_path):
            if not os.path.isdir(os.path.join(flow_nodes_path, node_dir)):
                continue

            try:
                module_name = f"flow_engine.flow_node.{node_dir}.{node_dir}"
                logger.info(f"Attempting to load module: {module_name}")
                module = importlib.import_module(module_name)
                logger.info(f"Successfully imported module: {module_name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, FlowNode)
                        and attr_name.endswith("Node")
                    ):
                        logger.info(f"Found Node class: {attr_name}")
                        if hasattr(attr, "_plugin_type"):
                            plugin_type = attr._plugin_type
                            cls._plugins[plugin_type] = attr
                            logger.info(f"Registered plugin: {plugin_type}")
                        else:
                            logger.warning(
                                f"Plugin class {attr_name} is not registered with @FlowNodeRegistry.register()"
                            )
            except Exception as e:
                logger.error(f"Error loading plugin from {node_dir}: {e}")
                continue

    @classmethod
    def register(cls, plugin_type: str):
        def decorator(plugin_class: Type[FlowNode]):
            logger.info(
                f"Registering plugin type: {plugin_type} for class: {plugin_class.__name__}"
            )
            plugin_class._plugin_type = plugin_type
            return plugin_class

        return decorator

    @classmethod
    def get_plugin(cls, plugin_type: str) -> Type[FlowNode]:
        if not cls._initialized:
            cls.initialize()

        if plugin_type not in cls._plugins:
            raise ValueError(
                f"Plugin type '{plugin_type}' not found in registry. Available plugins: {list(cls._plugins.keys())}"
            )
        return cls._plugins[plugin_type]

    @classmethod
    def get_available_plugins(cls) -> Dict[str, Type[FlowNode]]:
        if not cls._initialized:
            cls.initialize()
        return cls._plugins.copy()
