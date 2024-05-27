from fastapi import Depends

from api.modules.users.v1.dtos.user import UserDto
from api.modules.users.v1.repository import UsersRepository
from api.modules.users.v1.entities.user import User
from api.shared_resources.entities.paginated import Paginated


class UsersService:
    def __init__(self, users_repository: UsersRepository = Depends()) -> None:
        self.users_repository = users_repository

    async def read(self, parameters: UserDto.Read) -> Paginated[User]:
        return await self.users_repository.read(parameters)
