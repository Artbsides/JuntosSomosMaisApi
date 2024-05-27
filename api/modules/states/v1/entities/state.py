from typing import Type
from pydantic import Field, BaseModel, model_validator

from api.shared_resources.enums.regions import RegionsEnum


class State(BaseModel):
    id: int
    name: str = Field(alias="nome")
    region: RegionsEnum

    @model_validator(mode="before")
    @classmethod
    def format_data(cls: Type["State"], data: dict) -> dict:
        data.update({
            "region": str(data["regiao"]["nome"]).lower()
        })

        return data
