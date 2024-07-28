"""Request class for handling incoming requests."""

from typing import Dict
from dataclasses import dataclass


@dataclass
class Request:
    """A class representing a request."""
    query: Dict[str, str]
    body: bytes
    headers: Dict[str, str]

    @classmethod
    def from_environ(cls, environ: Dict):
        """Create a request from a WSGI environ."""
        query = {}
        if environ["QUERY_STRING"]:
            qs = environ["QUERY_STRING"]
            query = dict(entry.split("=") for entry in qs.split("&"))
        body = environ["wsgi.input"].read()
        headers = {
            k.replace("HTTP_", ""): v
            for k, v in environ.items()
            if k.startswith("HTTP_")
        }
        return cls(query, body, headers)
