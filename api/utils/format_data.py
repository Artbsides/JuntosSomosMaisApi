import re

from api.modules.users.v1.entities.user_location_cordinates import UserLocationCordinates
from api.modules.users.v1.enums.user_types import UserTypesEnum
from api.shared_resources.enums.countries import CountriesEnum


class FormatData:
    def nested_dicts(data, separator: str = "__"):
        if isinstance(data, (list, tuple)):
            return [
                FormatData.nested_dicts(value, separator) for value in data
            ]

        object = {}

        for key, value in data.items():
            if separator in key:
                principal, resto = key.split(separator, 1)

                object.update({
                    principal: FormatData.nested_dicts({**object.get(principal, {}), resto: value}, separator)
                })

            else:
                object.update({key: value})

        return object

    def type(coordinates: UserLocationCordinates):
        coordinate_ranges = {
            UserTypesEnum.normal: [
                {
                    "minlon": -26.155681,
                    "minlat": -54.777426,
                    "maxlon": -34.016466,
                    "maxlat": -46.603598
                }
            ],
            UserTypesEnum.special: [
                {
                    "minlon": -2.196998,
                    "minlat": -46.361899,
                    "maxlon": -15.411580,
                    "maxlat": -34.276938
                },
                {
                    "minlon": -19.766959,
                    "minlat": -52.997614,
                    "maxlon": -23.966413,
                    "maxlat": -44.428305
                }
            ]
        }

        for type, ranges in coordinate_ranges.items():
            for r in ranges:
                if r["maxlon"] <= coordinates.longitude <= r["minlon"] and r["minlat"] <= coordinates.latitude <= r["maxlat"]:
                    return type

        return UserTypesEnum.laborious

    def phone_number(number: str, ddi: str = CountriesEnum.DDI.br.value) -> str:
        return f"{ddi}{re.sub(r"\D", "", number)}"
