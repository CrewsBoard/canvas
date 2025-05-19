import logging
import os
from typing import Optional

from core.services.core import settings


class Logger(logging.Logger):
    def __init__(self, name: str, env: Optional[str] = None) -> None:
        super().__init__(name)

        self.disabled = not settings.server.debug
        self.env = env or os.getenv("ENVIRONMENT", "dev")
        log_level = logging.DEBUG if self.env == "dev" else logging.INFO
        self.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        self.addHandler(console_handler)


logger = Logger(__name__)
