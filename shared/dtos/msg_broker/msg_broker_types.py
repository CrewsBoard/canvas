from enum import Enum


class MsgBrokerTypes(str, Enum):
    REDIS = "redis"
    RABBITMQ = "rabbitmq"
