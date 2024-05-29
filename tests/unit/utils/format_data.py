from api.utils.format_data import FormatData
from api.modules.users.v1.enums.user_types import UserTypesEnum
from api.modules.users.v1.entities.user_location_cordinates import UserLocationCordinates


class TestFormatData:
    def nested_dict_successful_test(self) -> None:
        data = FormatData.nested_dicts([{
            "string": "string", "dictionary__integer": 1
        }])

        assert data == [{
            "string": "string", "dictionary": {
                "integer": 1
            }
        }]

    def type_succesful_test(self) -> None:
        assert FormatData.type(
            UserLocationCordinates(latitude=-47.336, longitude=-31.9196)
        ) is UserTypesEnum.normal

        assert FormatData.type(
            UserLocationCordinates(latitude=-36.7158, longitude=-9.1518)
        ), UserTypesEnum.special

        assert FormatData.type(
            UserLocationCordinates(latitude=-76.3253, longitude=137.9437)
        ), UserTypesEnum.laborious

    def phone_number_successful_test(self) -> None:
        assert FormatData.phone_number("12 4568-7898") == "+551245687898"
        assert FormatData.phone_number("(12)45687898") == "+551245687898"
