from typing import Optional
from pydantic import BaseModel, Field


class PaginationDto(BaseModel):
    pageSize: int = Field(ge=1, default=10)
    pageNumber: int = Field(ge=1, default=1)
