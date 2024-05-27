from typing import Optional
from pydantic import BaseModel

from api.shared_resources.enums.regions import RegionsEnum


class UserFilterLocationDto(BaseModel):
    region: Optional[RegionsEnum] = None
