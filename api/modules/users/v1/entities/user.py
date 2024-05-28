from typing import Type
from pydantic import BaseModel, model_validator

from api.utils.format_data import FormatData
from api.shared_resources.enums.countries import CountriesEnum
from api.modules.users.v1.entities.user_name import UserName
from api.modules.users.v1.entities.user_picture import UserPicture
from api.modules.users.v1.entities.user_location import UserLocation
from api.modules.users.v1.entities.user_location_cordinates import UserLocationCordinates


class User(BaseModel):
    type: str
    gender: str
    name: UserName
    location: UserLocation
    email: str
    birthday: str
    registered: str
    telephoneNumbers: list[str]
    mobileNumbers: list[str]
    picture: UserPicture
    nationality: str = CountriesEnum.Abreviation.br

    @model_validator(mode="before")
    @classmethod
    def format_data(cls: Type["User"], data: dict) -> dict:
        data.update({
            "type": FormatData.type(
                UserLocationCordinates(**data["location"]["coordinates"])
            ),
            "gender": "m" if data["gender"] == "male" else "f",
            "birthday": data["dob"]["date"],
            "registered": data["registered"]["date"],
            "telephoneNumbers": [
                FormatData.phone_number(data["phone"])
            ],
            "mobileNumbers": [
                FormatData.phone_number(data["cell"])
            ]
        })

        return data
