"""Log module."""

import datetime

from .wsgi import WSGIRequest, WSGIResponse


def log_request(client_address, request: WSGIRequest, response: WSGIResponse):
    """Print the request in log."""
    date_time = datetime.datetime.now()
    date_time_format = date_time.strftime("%d/%m/%Y %H:%M:%S")
    print(
        f"[{date_time_format}] {response.status} {request.http_method} {request.path} {client_address[0]} - {client_address[1]}"
    )
