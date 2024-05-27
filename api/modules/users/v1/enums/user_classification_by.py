from enum import Enum
from typing import Any, Type


class UserClassificationByEnum(Enum):
    name: tuple[str] = "first", "name.first"
    lastname: tuple[str] = "last", "name.last"
    gender: str = "gender"

    @classmethod
    def _missing_(cls: Type["UserClassificationByEnum"], value: Any) -> Type["UserClassificationByEnum"]:
        if value == "default":
            return cls.name

        return None
