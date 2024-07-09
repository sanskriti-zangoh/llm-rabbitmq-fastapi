import sys
from http import HTTPStatus
from typing import Dict


class Error(Exception):
    message: str = "Unexpected error occurred."
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str = None, *, detail: Dict = None, caught_exception: Exception = None) -> None:
        if message is not None:
            self.message = message
        if detail is not None:
            self.detail = detail
        else:
            self.detail = {}
        self.caught_exception = caught_exception or sys.exc_info()[1]

    def dict(self) -> Dict:
        return {
            "message": self.message,
            "detail": self.detail,
            "status_code": self.status_code
        }

class HTTPError(Error):
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR

class ServiceError(HTTPError):
    """Exception raised from service calls"""
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    message = "Service Error"