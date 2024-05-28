from typing import Type, Optional

from api.modules.users.v1.entities.user import User
from api.modules.states.v1.entities.state import State


class Storage:
    users: Optional[list[User]] = None
    states: Optional[list[State]] = None

    instance: Optional["Storage"] = None

    def __new__(cls) -> Type["Storage"]:
        if not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance
