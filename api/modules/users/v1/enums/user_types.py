from enum import Enum


class UserTypesEnum(str, Enum):
    normal: str = "normal"
    special: str = "special"
    laborious: str = "laborious"
