from pydantic import Field, BaseModel


class PaginationDto(BaseModel):
    pageSize: int = Field(ge=1, default=10)
    pageNumber: int = Field(ge=1, default=1)
