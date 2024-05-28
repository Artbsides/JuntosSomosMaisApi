from pydantic import BaseModel

from api.modules.users.v1.entities.user_location_timezone import UserLocationTimezone
from api.modules.users.v1.entities.user_location_cordinates import UserLocationCordinates


class UserLocation(BaseModel):
    region: str
    street: str
    city: str
    state: str
    postcode: int
    coordinates: UserLocationCordinates
    timezone: UserLocationTimezone
