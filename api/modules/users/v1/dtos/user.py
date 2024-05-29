from fastapi import Depends
from pydantic import BaseModel

from api.shared_resources.dtos.pagination import PaginationDto
from api.modules.users.v1.dtos.user_filter import UserFilterDto


class UserDto:
    class Read(BaseModel):
        filters: UserFilterDto = Depends()
        pagination: PaginationDto = Depends()
