from fastapi import Depends

from api.modules.users.v1.dtos.user import UserDto
from api.modules.users.v1.entities.user import User
from api.modules.users.v1.service import UsersService
from api.routers.router import router
from api.shared_resources.entities.paginated import Paginated


router_settings = {
    "tags": ["Users"], "response_model_by_alias": False
}


@router.get("/users", **router_settings)
async def read(parameters: UserDto.Read = Depends(), users_service: UsersService = Depends()) -> Paginated[User]:
    return await users_service.read(parameters)
