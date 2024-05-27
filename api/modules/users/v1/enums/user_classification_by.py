from enum import Enum
from typing import Any


class UserClassificationByEnum(Enum):
    name: tuple[str] = "first", "name.first"
    lastname: tuple[str] = "last", "name.last"
    gender: str = "gender"

    @classmethod
    def _missing_(self, value: Any) -> "UserClassificationByEnum":
        if value == "default":
            return self.name

        return None
