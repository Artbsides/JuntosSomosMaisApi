from api.shared_resources.enums.countries import CountriesEnum


class TestCountries:
    def ddi_successful_test(self) -> None:
        for ddi in CountriesEnum.DDI:
            assert isinstance(ddi.value, str)

    def abreviation_successful_test(self) -> None:
        for abreviation in CountriesEnum.Abreviation:
            assert isinstance(abreviation.value, str)
