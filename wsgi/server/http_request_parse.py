"""This module contains the HTTP-related enums."""

from .splitbuffer import SplitBuffer


class HttpRequestParser:
    """A class representing a HTTP request parser."""

    def __init__(self, protocol):
        self.protocol = protocol
        self.buffer = SplitBuffer()
        self.done_parsing_start = False
        self.done_parsing_headers = False
        self.expected_body_length = 0
        self.http_method = None
        self.http_version = None

    def feed_data(self, data: bytes):
        """Feed data to the parser."""
        self.buffer.feed_data(data)
        self.parse()

    def parse(self):
        """Parse the data in the buffer."""
        if not self.done_parsing_start:
            self.parse_startline()
        elif not self.done_parsing_headers:
            self.parse_headerline()
        elif self.expected_body_length:
            data = self.buffer.flush()
            self.expected_body_length -= len(data)
            self.protocol.on_body(data)
            self.parse()
        else:
            self.protocol.on_message_complete()

    def parse_startline(self):
        """Parse the start line of the HTTP request."""
        line = self.buffer.pop(separator=b"\r\n")
        if line is not None:
            http_method, url, http_version = line.strip().split()
            self.http_method = http_method
            self.http_version = http_version
            self.done_parsing_start = True
            self.protocol.on_url(url)
            self.parse()

    def parse_headerline(self):
        """Parse the header line of the HTTP request."""
        line = self.buffer.pop(separator=b"\r\n")
        if line is not None:
            if line:
                name, value = line.strip().split(b": ", maxsplit=1)
                if name.lower() == b"content-length":
                    self.expected_body_length = int(value.decode("utf-8"))
                self.protocol.on_header(name, value)
            else:
                self.done_parsing_headers = True
            self.parse()
