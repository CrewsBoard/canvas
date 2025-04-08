import os
from pathlib import Path

import yaml
from pydantic_settings import BaseSettings

from core.dtos.settings import SettingsDto


class SettingsService(BaseSettings, SettingsDto):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            cls.yaml_config_source(),
            env_settings,
            init_settings,
            file_secret_settings,
        )

    @classmethod
    def yaml_config_source(cls):
        settings_type: str = os.environ.get("ENVIRONMENT", "dev")
        current_file_path = os.path.abspath(__file__).split("src")
        current_file_path = current_file_path[:-1][0]
        settings_dir = os.path.join(current_file_path, "src", "core", "configs")
        settings_path = os.path.join(settings_dir, f"{settings_type}.yaml")
        config_path = Path(settings_path)
        if config_path.exists():
            with config_path.open("r") as f:
                data = yaml.safe_load(f)
            data["settings_type"] = settings_type
            data["settings_dir"] = settings_dir
            return lambda: data
        return lambda: {}
