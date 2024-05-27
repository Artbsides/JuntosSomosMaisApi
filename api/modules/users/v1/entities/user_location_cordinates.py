from pydantic import BaseModel


class UserLocationCordinates(BaseModel):
    latitude: float
    longitude: float
