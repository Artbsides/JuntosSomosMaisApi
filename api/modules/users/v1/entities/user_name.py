from pydantic import BaseModel


class UserName(BaseModel):
    title: str
    first: str
    last: str
