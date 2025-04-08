from enum import Enum


class CodeExecutionModes(str, Enum):
    SAFE = "safe"
    UNSAFE = "unsafe"
