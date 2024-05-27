from enum import Enum


class CountriesEnum:
    class DDI(str, Enum):
        br: str = "+55"

    class Abreviation(str, Enum):
        br: str = "BR"
