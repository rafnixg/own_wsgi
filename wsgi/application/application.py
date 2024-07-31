"""A module for the WSGI application class."""

import sys

from typing import Callable
from dataclasses import dataclass
from .request import Request
from .response import PlainTextResponse, BaseResponse, JSONResponse


@dataclass(frozen=True, eq=True)
class PathOperation:
    """A class representing a path operation."""

    path: str
    http_method: str


class WSGIApplication:
    """A class representing a WSGI application."""

    def __init__(self):
        self.path_operations = dict()
        self.app_dir = self._get_app_dir()
        self.template_dir = f"{self.app_dir}/templates"

    def _get_app_dir(self):
        return sys.path[0]

    def _register_path_operation(self, path: str, http_method: str, func: Callable):
        po = PathOperation(path, http_method)
        self.path_operations[po] = func

    def _create_register_decorator(self, path: str, http_method: str):
        def decorator(func: Callable):
            self._register_path_operation(path, http_method, func)
            return func

        return decorator

    def get(self, path: str):
        """Register a GET handler."""
        return self._create_register_decorator(path, "GET")

    def post(self, path: str):
        """Register a POST handler."""
        return self._create_register_decorator(path, "POST")

    def put(self, path: str):
        """Register a PUT handler."""
        return self._create_register_decorator(path, "PUT")

    def delete(self, path: str):
        """Register a DELETE handler."""
        return self._create_register_decorator(path, "DELETE")

    def _get_path_operation(self, path: str, http_method: str):
        path = path.rstrip("/")
        po = PathOperation(path, http_method)
        return self.path_operations.get(po)

    def __call__(self, environ, start_response):
        func = self._get_path_operation(environ["PATH_INFO"], environ["REQUEST_METHOD"])
        if func is None:
            response = PlainTextResponse(status="404 NOT FOUND")
        else:
            request = Request.from_environ(environ)
            ret = func(request=request)
            if isinstance(ret, BaseResponse):
                response = ret
            elif isinstance(ret, dict):
                response = JSONResponse(body=ret)
            else:
                response = PlainTextResponse(body=ret)
        start_response(response.status, response.headers)
        return [response.body]
