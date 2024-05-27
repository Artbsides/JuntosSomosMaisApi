from pydantic import BaseModel


class UserPicture(BaseModel):
    large: str
    medium: str
    thumbnail: str
