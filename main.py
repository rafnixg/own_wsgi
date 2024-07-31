"""A simple WSGI application example."""

from wsgi.application.template import Template
from wsgi.server import WSGIServer
from wsgi.application import WSGIApplication
from wsgi.application.request import Request
from wsgi.application.response import (
    PlainTextResponse,
    HTMLResponse,
    JSONResponse,
    TemplateResponse,
)
from wsgi.application.middleware import timing_middleware

# Create a WSGI application
app = WSGIApplication(
    middleware=[
        timing_middleware,
    ]
)

# Register path operations


@app.get("/")
def index(request: Request) -> PlainTextResponse:
    """Index page."""
    return PlainTextResponse(status="200 OK", body="Hello, World!")


@app.get("/html")
def html(request: Request) -> HTMLResponse:
    """HTML page."""
    return HTMLResponse(body="<h1>Hello, World!</h1>", status="200 OK")


@app.get("/json")
def json(request: Request) -> JSONResponse:
    """JSON page."""
    return JSONResponse(body={"message": "Hello, World!"})


@app.post("/echo")
def echo(request: Request) -> PlainTextResponse:
    """Echo page."""
    return PlainTextResponse(body=request.body.decode("utf-8"))


@app.get("/template")
def template(request: Request) -> HTMLResponse:
    """Template page."""
    template_path = (
        "index.html"
        if request.query.get("name") is None
        else request.query.get("name") + ".html"
    )
    context = {"message": "Hello, World! from context"}
    # This is a simple way to render a template, is like a jinja2 template engine.
    # In a real-world application, you should use a template engine.
    render_template = Template(template_path).render(**context)
    if not render_template:
        return HTMLResponse(status="404 NOT FOUND", body="Not Found")

    return TemplateResponse(template=template_path, context=context)


if __name__ == "__main__":
    # Create a server
    server = WSGIServer("localhost", 8081, app)
    # Run the server
    server.server_forever()
