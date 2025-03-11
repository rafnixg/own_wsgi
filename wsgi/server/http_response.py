"""Create a HTTP response."""

from typing import List, Tuple


def create_status_line(status: str = "200 OK") -> str:
    """Create the status line for the HTTP response.
    Args:
        status (str): The status.
    Returns:
        str: The formatted status line.
    """
    return f"HTTP/1.1 {status}\r\n"


def format_headers(headers: List[Tuple[str, str]]) -> str:
    """Format the headers for the HTTP response.
    Args:
        headers (list): The headers.
    Returns:
        str: The formatted headers.
    """
    return "".join([f"{key}: {value}\r\n" for key, value in headers])


def make_response(
    status: str = "200 OK",
    headers: List[Tuple[str, str]] = None,
    body: bytes = b"",
):
    """Create a HTTP response from the status, headers, and body.
    Args:
        status (str): The status.
        headers (list): The headers.
        body (bytes): The body.
    Returns:
        bytes: The HTTP response.
    """
    if headers is None:
        headers = []
    content = [
        create_status_line(status).encode("utf-8"),
        format_headers(headers).encode("utf-8"),
        b"\r\n" if body else b"",
        body,
    ]
    return b"".join(content)
