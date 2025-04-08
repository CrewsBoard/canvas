from core.dtos.settings import ServerSettingsDto, DatabaseSettingsDto


class SettingsDto:
    settings_type: str
    settings_dir: str
    server: ServerSettingsDto
    database: DatabaseSettingsDto
