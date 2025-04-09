from typing import Dict, Type

from flow_engine.flow_chain.services.plugin_base import FlowNode


class PluginRegistry:
    _instance = None
    _plugins: Dict[str, Type[FlowNode]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PluginRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, plugin_type: str):
        def decorator(plugin_class: Type[FlowNode]):
            cls._plugins[plugin_type] = plugin_class
            return plugin_class

        return decorator

    @classmethod
    def get_plugin(cls, plugin_type: str) -> Type[FlowNode]:
        if plugin_type not in cls._plugins:
            raise ValueError(f"Plugin type '{plugin_type}' not found in registry")
        return cls._plugins[plugin_type]

    @classmethod
    def get_available_plugins(cls) -> Dict[str, Type[FlowNode]]:
        return cls._plugins.copy()
