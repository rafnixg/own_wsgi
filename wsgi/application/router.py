"""A module for the router class."""
from typing import Callable
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Routes:
    """A class representing a route."""

    path: str
    http_method: str

    def __hash__(self):
        return hash((self.path, self.http_method))

    def __eq__(self, other):
        return self.path == other.path and self.http_method == other.http_method

    def __ne__(self, other):
        return not self.__eq__(other)


class Router:
    """A class representing a router."""

    def __init__(self):
        self.routes = dict()

    def register(self, path: str, http_method: str, func: Callable):
        """Register a path operation.
        Args:
            path (str): The path.
            http_method (str): The HTTP method.
            func (Callable): The function to call.
        """
        route = Routes(path, http_method)
        self.routes[route] = func

    def get(self, path: str):
        """Register a GET handler.
        Args:
            path (str): The path.
        """

        def decorator(func: Callable):
            self.register(path, "GET", func)
            return func

        return decorator

    def post(self, path: str):
        """Register a POST handler.
        Args:
            path (str): The path.
        """

        def decorator(func: Callable):
            self.register(path, "POST", func)
            return func

        return decorator

    def put(self, path: str):
        """Register a PUT handler.
        Args:
            path (str): The path.
        """

        def decorator(func: Callable):
            self.register(path, "PUT", func)
            return func

        return decorator

    def delete(self, path: str):
        """Register a DELETE handler.
        Args:
            path (str): The path.
        """

        def decorator(func: Callable):
            self.register(path, "DELETE", func)
            return func

        return decorator

    def get_route_handler(self, path: str, http_method: str):
        """Get the path operation. 
        Args:
            path (str): The path.
            http_method (str): The HTTP method.
        """
        path = path.rstrip("/") if path != "/" else path
        route = Routes(path, http_method)
        return self.routes.get(route)
