"""Log Middleware."""

import datetime
import logging

from .wsgi import WSGIRequest, WSGIResponse


def log_output(func):
    """Log the request and response."""

    def wrapper(*args, **kwargs):
        client_address = args[0].client_address
        request = args[0].request
        response = args[0].response
        log_request(client_address, request, response)
        return func(*args, **kwargs)

    return wrapper


def print_log(message: str, error: bool = False):
    """Print the message in log.
    Args:
        message (str): The message to print.
    """
    date_time = datetime.datetime.now()
    date_time_format = date_time.strftime("%d/%m/%Y %H:%M:%S")
    log_message = f"[{date_time_format}] {message}"
    print(log_message)
    if error:
        logging.error(log_message)
    else:
        logging.info(log_message)

def log_request(client_address, request: WSGIRequest, response: WSGIResponse):
    """Print the request in log.
    Args:
        client_address (tuple): The client address.
        request (WSGIRequest): The request object.
        response (WSGIResponse): The response object.
    """
    log_message = f"{response.status} {request.http_method} {request.path} {client_address[0]} - {client_address[1]}"
    print_log(log_message)
