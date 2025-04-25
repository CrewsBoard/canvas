from .database_settings_dto import DatabaseSettingsDto
from .msg_broker_settings_dto import MsgBrokerSettingsDto
from .server_settings_dto import ServerSettingsDto


class SettingsDto:
    settings_type: str
    settings_dir: str
    server: ServerSettingsDto
    database: DatabaseSettingsDto
    msg_broker: MsgBrokerSettingsDto
