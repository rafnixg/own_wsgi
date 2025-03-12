"""A simple WSGI application example."""

from wsgi.server import WSGIServer
from wsgi.application import WSGIApplication
from wsgi.application.request import Request
from wsgi.application.response import (
    PlainTextResponse,
    HTMLResponse,
    JSONResponse,
    NotFoundResponse,
    HTTPErrorResponse,
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
    routes = [route.path for route in app.router.routes]
    return PlainTextResponse(
        status="200 OK", body="\n".join(routes) if routes else "No routes found."
    )


@app.get("/html")
def html(request: Request) -> HTMLResponse:
    """HTML page."""
    routes = [f'<li><a href="{route.path}">{route.path}</a></li>' for route in app.router.routes]
    routes_html = f'<ul>{"".join(routes)}</ul>'
    return HTMLResponse(body=f"<h1>Hello, World!</h1>{routes_html}", status="200 OK")


@app.get("/json")
def json(request: Request) -> JSONResponse:
    """JSON page."""
    if request.query.get("name") is not None:
        return JSONResponse(body={"message": f"Hello, {request.query.get('name')}!"})
    if request.query.get("error") is not None:
        return HTTPErrorResponse(
            status="500 INTERNAL SERVER ERROR", body="Internal Server Error"
        )
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
    render_template = app.template_engine(template_path).render(**context)
    if not render_template:
        return NotFoundResponse()
    return HTMLResponse(body=render_template)


if __name__ == "__main__":
    # Create a server
    server = WSGIServer("0.0.0.0", 8081, app)
    # Run the server
    server.server_forever()
