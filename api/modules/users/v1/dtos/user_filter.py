from typing import Optional
from fastapi import Depends
from pydantic import BaseModel

from api.modules.users.v1.dtos.user_filter_location import UserFilterLocationDto
from api.modules.users.v1.enums.user_types import UserTypesEnum


class UserFilterDto(BaseModel):
    type: Optional[UserTypesEnum] = None
    location: UserFilterLocationDto = Depends()
