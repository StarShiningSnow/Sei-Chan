from enum import StrEnum

class AIMode(StrEnum):
    ASK = "ask"
    MC = "mc"
    MAP = "map"
    INTRO = "intro"

class AIRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"