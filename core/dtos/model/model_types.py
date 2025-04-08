from enum import Enum


class ModelTypes(str, Enum):
    INFERENCE = "inference"
    EMBEDDING = "embedding"
