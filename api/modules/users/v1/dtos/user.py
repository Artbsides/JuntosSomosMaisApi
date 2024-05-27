from fastapi import Depends
from pydantic import BaseModel

from api.shared_resources.dtos.pagination import PaginationDto
from api.modules.users.v1.dtos.user_filter import UserFilterDto
from api.shared_resources.dtos.classification import ClassificationDto
from api.modules.users.v1.enums.user_classification_by import UserClassificationByEnum


class UserDto:
    class Read(BaseModel):
        filters: UserFilterDto = Depends()
        classification: ClassificationDto[UserClassificationByEnum] = Depends()
        pagination: PaginationDto = Depends()
