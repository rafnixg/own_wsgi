"""Response classes for the application."""

import json

from typing import List, Tuple, Optional, Any

from wsgi.application.template import TemplateParser


class BaseResponse:
    """Base response class for the application."""

    def __init__(
        self,
        status: str = "200 OK",
        headers: Optional[List[Tuple[str, str]]] = None,
        body: Optional[Any] = None,
        content_type: Optional[str] = None,
    ):
        self.status = status
        self.headers = headers if headers is not None else []
        self.body = self.body_conversion(body) if body is not None else b""
        self.content_type = content_type if content_type is not None else "text/plain"
        self.add_content_type_and_content_length()

    def add_content_type_and_content_length(self):
        """Add the Content-Type and Content-Length headers."""
        header_names = {name for name, value in self.headers}
        if not "Content-Type" in header_names:
            self.headers.append(("Content-Type", self.content_type))
        if self.body and not "Content-Length" in header_names:
            self.headers.append(("Content-Length", str(len(self.body))))

    @classmethod
    def body_conversion(cls, body):
        """Convert the body to bytes."""
        return body


class PlainTextResponse(BaseResponse):
    """A plain text response class for the application."""

    content_type = "text/plain"

    def __init__(
        self,
        status: str = "200 OK",
        headers: Optional[List[Tuple[str, str]]] = None,
        body: Optional[Any] = None,
    ):
        super().__init__(status, headers, body)

    @classmethod
    def body_conversion(cls, body):
        return body.encode("utf-8")


class HTMLResponse(BaseResponse):
    """An HTML response class for the application."""

    content_type = "text/html"

    def __init__(
        self,
        status: str = "200 OK",
        headers: Optional[List[Tuple[str, str]]] = None,
        body: Optional[Any] = None,
    ):
        super().__init__(status, headers, body, self.content_type)

    @classmethod
    def body_conversion(cls, body):
        return body.encode("utf-8")


class JSONResponse(BaseResponse):
    """A JSON response class for the application."""

    content_type = "application/json"

    def __init__(
        self,
        status: str = "200 OK",
        headers: Optional[List[Tuple[str, str]]] = None,
        body: Optional[Any] = None,
    ):
        super().__init__(status, headers, body, self.content_type)

    @classmethod
    def body_conversion(cls, body):
        return json.dumps(body).encode("utf-8")


class TemplateResponse(HTMLResponse):
    """A template response class for the application."""

    content_type = "text/html"

    def __init__(
        self,
        status: str = "200 OK",
        headers: Optional[List[Tuple[str, str]]] = None,
        body: Optional[Any] = None,
        template: str = "",
        context: Optional[dict] = None,
    ):
        self.template = template
        self.context = context if context is not None else {}
        super().__init__(status, headers, body)

    def render_template(self):
        """Render the template."""
        template_parser = TemplateParser(self.template, self.context)
        parse_template = template_parser.parse()
        if not parse_template:
            self.status = "404 NOT FOUND"
            return f"Template not found: {self.template}"
        return parse_template

    def add_content_type_and_content_length(self):
        """Add the Content-Type and Content-Length headers."""
        self.body = self.render_template().encode("utf-8")
        super().add_content_type_and_content_length()
