from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

from api.shared_resources.enums.classification_direction import ClassificationDirectionEnum


EntityClassification = TypeVar("EntityClassification")


class ClassificationDto(BaseModel, Generic[EntityClassification]):
    order_by: EntityClassification = "default"
    order_direction: Optional[ClassificationDirectionEnum] = ClassificationDirectionEnum.desc
