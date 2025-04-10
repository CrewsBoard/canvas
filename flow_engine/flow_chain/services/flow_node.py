from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from shared.services.context_manager import ContextManager


class FlowNode(ABC, ContextManager):
    def __init__(
        self, name: str, node_type: str, configuration: Optional[Dict[str, Any]] = None
    ):
        super().__init__()
        self.id = str(id(self))
        self.name = name
        self.type = node_type
        self.configuration = configuration or {}

    @abstractmethod
    def process(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the incoming message and return the result.
        This method must be implemented by all flow nodes.
        """
        pass

    def validate_configuration(self) -> bool:
        """
        Validate the node's configuration.
        Returns True if configuration is valid, False otherwise.
        """
        return True

    def get_metadata(self) -> Dict[str, Any]:
        """
        Return metadata about the node.
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "configuration": self.configuration,
        }
