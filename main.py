"""A simple HTTP server."""

from wsgi.server import WSGIServer
from wsgi.application import WSGIApplication
from wsgi.application.request import Request
from wsgi.application.response import PlainTextResponse, HTMLResponse, JSONResponse

# Create a WSGI application
app = WSGIApplication()

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

# Set the application

if __name__ == "__main__":
    # Create a server
    server = WSGIServer("localhost", 4221, app)
    # Run the server
    server.server_forever()
