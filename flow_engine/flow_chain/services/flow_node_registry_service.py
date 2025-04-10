import importlib
import os
from typing import Dict, Type, List

from flow_engine.flow_chain.dtos import FlowNode
from shared.utils.funcs import get_root_path
from shared.utils import logger


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
        """Explicitly initialize the registry and load plugins."""
        if not cls._initialized:
            logger.info("Initializing FlowNodeRegistry...")
            cls._load_all_plugins()
            cls._initialized = True
            logger.info(f"FlowNodeRegistry initialized with plugins: {list(cls._plugins.keys())}")

    @classmethod
    def _load_all_plugins(cls) -> None:
        """Dynamically load all plugin modules from the flow_node directory."""
        flow_nodes_path = os.path.join(get_root_path(), "flow_engine", "flow_node")
        logger.info(f"Loading plugins from: {flow_nodes_path}")
        
        for node_dir in os.listdir(flow_nodes_path):
            if not os.path.isdir(os.path.join(flow_nodes_path, node_dir)):
                continue
                
            try:
                module_name = f"flow_engine.flow_node.{node_dir}.{node_dir}"
                logger.info(f"Attempting to load module: {module_name}")
                module = importlib.import_module(module_name)
                
                # Find the plugin class (class that ends with 'Node')
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, FlowNode) and attr_name.endswith('Node'):
                        # The plugin type is determined by the class name without 'Node' suffix
                        plugin_type = attr_name[:-4].lower()
                        cls._plugins[plugin_type] = attr
                        logger.info(f"Registered plugin: {plugin_type}")
            except Exception as e:
                logger.error(f"Error loading plugin from {node_dir}: {e}")
                continue

    @classmethod
    def register(cls, plugin_type: str):
        def decorator(plugin_class: Type[FlowNode]):
            cls._plugins[plugin_type] = plugin_class
            return plugin_class

        return decorator

    @classmethod
    def get_plugin(cls, plugin_type: str) -> Type[FlowNode]:
        if not cls._initialized:
            cls.initialize()
            
        if plugin_type not in cls._plugins:
            raise ValueError(f"Plugin type '{plugin_type}' not found in registry. Available plugins: {list(cls._plugins.keys())}")
        return cls._plugins[plugin_type]

    @classmethod
    def get_available_plugins(cls) -> Dict[str, Type[FlowNode]]:
        if not cls._initialized:
            cls.initialize()
        return cls._plugins.copy()
