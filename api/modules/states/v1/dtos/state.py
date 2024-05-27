from typing import Optional
from pydantic import BaseModel


class StateDto:
    class Create(BaseModel):
        name: str
        region: Optional[str] = None

    class ReadOne(BaseModel):
        name: str = None
