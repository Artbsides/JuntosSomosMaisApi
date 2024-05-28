from typing import Optional


class ApiBaseException(BaseException):
    args: Optional[dict[str, str]] = None
    status_code: int
