from .database_settings_dto import DatabaseSettingsDto
from .flow_engine_settings_dto import FlowEngineSettingsDto
from .flow_nodes_settings_dto import FlowNodesSettingsDto
from .msg_broker_settings_dto import MsgBrokerSettingsDto
from .server_settings_dto import ServerSettingsDto


class SettingsDto:
    settings_type: str
    settings_dir: str
    server: ServerSettingsDto
    database: DatabaseSettingsDto
    msg_broker: MsgBrokerSettingsDto
    flow_engine: FlowEngineSettingsDto
    flow_nodes: FlowNodesSettingsDto
