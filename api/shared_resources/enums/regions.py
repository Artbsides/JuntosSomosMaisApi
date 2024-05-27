from enum import Enum


class RegionsEnum(str, Enum):
    north: str = "norte"
    northeast: str = "nordeste"
    midwest: str = "centro-oeste"
    southeast: str = "sudeste"
    south: str = "sul"
