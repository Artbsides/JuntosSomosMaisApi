from pydantic import BaseModel

from api.modules.users.v1.entities.user_location_cordinates import UserLocationCordinates
from api.modules.users.v1.entities.user_location_timezone import UserLocationTimezone


class UserLocation(BaseModel):
    region: str
    street: str
    city: str
    state: str
    postcode: int
    coordinates: UserLocationCordinates
    timezone: UserLocationTimezone
