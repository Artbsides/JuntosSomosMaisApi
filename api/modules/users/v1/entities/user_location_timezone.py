from pydantic import BaseModel


class UserLocationTimezone(BaseModel):
    offset: str
    description: str
