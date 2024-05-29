from api.shared_resources.enums.regions import RegionsEnum


class TestRegions:
    def regions_successful_test(self) -> None:
        for region in RegionsEnum:
            assert isinstance(region.value, str)
