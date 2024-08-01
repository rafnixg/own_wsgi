"""A module containing the WSGI server implementation."""

import socket
import threading
import sys

from .constant import BUFFER_ZISE
from .wsgi import WSGIResponse, WSGIRequest
from .http_request_parse import HttpRequestParser
from .log import log_request
from .utils import print_welcome_message


class WSGIServer:
    """A class representing a WSGI server."""

    def __init__(
        self, host: str = "localhost", port: int = 8080, app: callable = None
    ) -> None:
        self.host = host
        self.port = port
        self.app = app

        if self.app is None:
            # TODO: run the server statically without an app
            print("Please provide a WSGI application.")
            sys.exit(1)

    def server_forever(self):
        """Run the server."""
        # Create a TCP server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP
        server_socket.bind((self.host, self.port))  # Bind the socket to the address
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # Reuse the address
        server_socket.listen(1)  # Listen for incoming connections
        # Print the welcome message
        self.app.host = self.host
        self.app.port = self.port
        print_welcome_message(self.app)
        # Keep the server running forever
        while True:
            try:
                # Accept the connection from TCP client
                client_socket, client_address = server_socket.accept()
                print(f"Socket established with {client_address}.")
                # Create a session for the client
                session = Session(client_socket, client_address, self.app)
                # Create a thread to handle the client connection
                thread = threading.Thread(
                    target=session.run,
                )
                # Start the thread
                thread.start()
            except KeyboardInterrupt:
                print("Server is shutting down.")
                server_socket.close()
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                server_socket.close()
                break
        # Close the server socket
        server_socket.close()
        # Print the server shutdown message
        print("Server has been shutdown.")
        sys.exit(0)  # Exit the program


class Session:
    """A class representing a session."""

    def __init__(
        self, client_socket: socket.socket, client_address: tuple, app: callable
    ) -> None:
        self.client_socket = client_socket
        self.client_address = client_address
        self.app = app
        self.parser = HttpRequestParser(self)
        self.response = WSGIResponse()
        self.request = WSGIRequest()

    def run(self):
        """Run the server."""
        while True:
            if self.response.is_sent:
                break
            data = self.client_socket.recv(BUFFER_ZISE)
            self.parser.feed_data(data)
        self.client_socket.close()
        print(f"Socket closed with {self.client_address}.")

    def on_url(self, url: bytes):
        """Handle the URL callback."""
        print(f"Received url: {url}")
        self.request.http_method = self.parser.http_method.decode("utf-8")
        self.request.path = url.decode("utf-8")

    def on_header(self, name: bytes, value: bytes):
        """Handle the header callback."""
        # print(f"Received header: ({name}, {value})")
        self.request.headers.append((name.decode("utf-8"), value.decode("utf-8")))

    def on_body(self, body: bytes):
        """Handle the body callback."""
        # print(f"Received body: {body}")
        self.request.body.write(body)
        self.request.body.seek(0)

    def on_message_complete(self):
        """Handle the message complete callback"""
        print("Received request completely.")
        environ = self.request.to_environ()
        body_chunks = self.app(environ, self.response.start_response)
        # print("App callable has returned.")
        self.response.body = b"".join(body_chunks)
        self.client_socket.send(self.response.to_http())
        log_request(self.client_address, self.request, self.response)
