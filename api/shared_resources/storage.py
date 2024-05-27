from typing import Optional

from api.modules.states.v1.entities.state import State
from api.modules.users.v1.entities.user import User


class Storage:
    users: Optional[list[User]] = None
    states: Optional[list[State]] = None

    instance: Optional["Storage"] = None

    def __new__(self) -> "Storage":
        if not self.instance:
            self.instance = super(Storage, self).__new__(self)

        return self.instance
