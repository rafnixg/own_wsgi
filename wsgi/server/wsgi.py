"""A module for WSGI request and response classes."""

from dataclasses import dataclass, field
from typing import List, Tuple

from io import BytesIO
from .http_response import make_response


@dataclass
class WSGIRequest:
    """A class representing a WSGI request."""

    http_method: str = ""
    path: str = ""
    headers: List[Tuple[str, str]] = field(default_factory=lambda: [])
    body: BytesIO = BytesIO()

    def to_environ(self):
        """Convert the request to a WSGI environ."""
        path_parts = self.path.split("?")
        headers_dict = {k: v for k, v in self.headers}
        environ = {
            "REQUEST_METHOD": self.http_method,
            "PATH_INFO": path_parts[0],
            "QUERY_STRING": path_parts[1] if len(path_parts) > 1 else "",
            "SERVER_NAME": "127.0.0.1",
            "SERVER_PORT": "5000",
            "SERVER_PROTOCOL": "HTTP/1.1",
            "CONTENT_TYPE": headers_dict.get("Content-Type", ""),
            "CONTENT_LENGTH": headers_dict.get("Content-Length", ""),
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": self.body,
            "wsgi.errors": BytesIO(),
            "wsgi.multithread": True,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
            **{f"HTTP_{name}": value for name, value in self.headers},
        }
        return environ


@dataclass
class WSGIResponse:
    """A class representing a WSGI response."""

    status: str = ""
    headers: List[Tuple[str, str]] = field(default_factory=lambda: [])
    body: BytesIO = BytesIO()
    is_sent: bool = False

    def start_response(
        self, status: str, headers: List[Tuple[str, str]], exc_info=None
    ):
        """Start the response with the status and headers."""
        print("Start response with", status, headers)
        self.status = status
        self.headers = headers

    def to_http(self):
        """Convert the response to a HTTP response message."""
        self.is_sent = True
        return make_response(self.status, self.headers, self.body)
