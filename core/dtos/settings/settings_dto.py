from core.dtos.settings.database_settings_dto import DatabaseSettingsDto
from core.dtos.settings.msg_broker_settings_dto import MsgBrokerSettingsDto
from core.dtos.settings.server_settings_dto import ServerSettingsDto


class SettingsDto:
    settings_type: str
    settings_dir: str
    server: ServerSettingsDto
    database: DatabaseSettingsDto
    msg_broker: MsgBrokerSettingsDto
