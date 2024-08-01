"""A module for the WSGI application class."""

import sys


from .router import Router
from .template import Template
from .request import Request
from .response import PlainTextResponse, BaseResponse, JSONResponse, NotFoundResponse


class WSGIApplication:
    """A class representing a WSGI application."""

    def __init__(
        self, middleware: list[callable] = None, template_engine: object = None
    ):
        """Initialize the WSGI application.
        Args:
            middleware (list[callable], optional): The middleware. Defaults to None.
            template_engine (object, optional): The template engine. Defaults to None.
        """
        self.router = Router()
        self.app_dir = self._get_app_dir()
        self.middleware = middleware
        self.template_engine = (
            template_engine if template_engine is not None else Template
        )

    def _get_app_dir(self):
        return sys.path[0]

    def get(self, path: str):
        """Register a GET handler.
        Args:
            path (str): The path.
        """
        return self.router.get(path)

    def post(self, path: str):
        """Register a POST handler.
        Args:
            path (str): The path.
        """
        return self.router.post(path)

    def put(self, path: str):
        """Register a PUT handler.
        Args:
            path (str): The path.
        """
        return self.router.put(path)

    def delete(self, path: str):
        """Register a DELETE handler.
        Args:
            path (str): The path.
        """
        return self.router.delete(path)

    def __call__(self, environ, start_response):
        route_handler = self.router.get_route_handler(
            environ["PATH_INFO"], environ["REQUEST_METHOD"]
        )
        if route_handler is None:
            response = NotFoundResponse()
        else:
            route_handler = self.apply_middleware(route_handler)
            request = Request.from_environ(environ)
            response = route_handler(request=request)
            if isinstance(response, dict):
                response = JSONResponse(body=response)
            elif not isinstance(response, BaseResponse):
                response = PlainTextResponse(body=response)
        start_response(response.status, response.headers)
        return [response.body]

    def apply_middleware(self, func):
        """Apply middleware to the function."""
        if self.middleware is not None:
            for middleware in self.middleware:
                func = middleware(func)
        return func
