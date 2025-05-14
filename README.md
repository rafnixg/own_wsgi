[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/rafnixg/own_wsgi)

# Tutorial: Own WSGI Server.

This is a simple tutorial on how to create your own WSGI server. This tutorial is for educational purposes only. It is not recommended to use this server in production.

## What is WSGI?

WSGI stands for Web Server Gateway Interface. It is a specification that describes how a web server communicates with web applications. WSGI is a standard interface between web servers and Python web frameworks or applications. It allows you to write web applications independently of the web server.
PEP 3333 is the official specification for WSGI in Python. (https://www.python.org/dev/peps/pep-3333/)[https://www.python.org/dev/peps/pep-3333/]

## Parts of a WSGI Server

A WSGI server consists of two main parts:

1. Web Server: The web server is responsible for accepting incoming HTTP requests and passing them to the WSGI application.

2. WSGI Application: The WSGI application is a Python callable that takes two arguments: `environ` and `start_response`. The `environ` argument is a dictionary containing the HTTP request information, and the `start_response` argument is a callable that is used to send the HTTP response headers.

### Web Server

The web server is responsible for accepting incoming HTTP requests and passing them to the WSGI application. The web server can be implemented using the `socket` module in Python. The web server listens on a specific port for incoming connections and processes the requests.

### WSGI Application

The WSGI application is a Python callable that takes two arguments: `environ` and `start_response`. The `environ` argument is a dictionary containing the HTTP request information, and the `start_response` argument is a callable that is used to send the HTTP response headers.

- `environ`: A dictionary containing the HTTP request information, such as the request method, request URL, and request headers.
- `start_response`: A callable that takes two arguments: `status` and `headers`. The `status` argument is a string containing the HTTP status code and message, and the `headers` argument is a list of tuples containing the HTTP response headers.

The WSGI application must return an iterable object that contains the response body content. The response body content can be a string, a list of strings, or a file-like object.

### WSGI Application Framework

A WSGI application framework is a library or module that provides utilities and tools for building WSGI applications. It typically includes features such as routing, middleware, request and response objects, and error handling.

Features of a WSGI application framework:

- [x] Routing: The framework provides a way to map URLs to specific functions or handlers.
- [x] Middleware: The framework allows you to add middleware functions to process requests and responses.
- [x] Request and Response Objects: The framework provides request and response objects to access the HTTP request and response data.
- [-] Error Handling: The framework provides a way to handle errors and exceptions in the application.
- [x] Utilities: The framework provides utilities and tools to simplify common tasks in web development.



## Own WSGI Server

### Using Own WSGI Application Framework

how to use the server module with the application module to create a simple WSGI server that responds with different types of content based on the request URL.

```python
"""A simple HTTP server."""

from wsgi.server import WSGIServer
from wsgi.application import WSGIApplication
from wsgi.application.request import Request
from wsgi.application.response import PlainTextResponse, HTMLResponse, JSONResponse

# Create a WSGI application
app = WSGIApplication()

# Define a simple WSGI application
@app.route('/')
def hello(request):
    return PlainTextResponse(body='Hello, World!')

@app.route('/html')
def html(request):
    return HTMLResponse(body='<h1>Hello, World!</h1>')

@app.route('/json')
def json(request):
    return JSONResponse(body={'message': 'Hello, World!'})

# Create a WSGI server
server = WSGIServer(host='localhost', port=8000, app)

# Start the server
server.serve_forever()
```

To run the server, save the code to a file named `app.py` and run it using the following command:

```bash
python app.py
```

The server will start listening on port 8000. You can test the server by opening a web browser and navigating to `http://localhost:8000`, `http://localhost:8000/html`, or `http://localhost:8000/json`. You should see different types of content displayed in the browser.

### Using FastAPI

```python

from fastapi import FastAPI
from wsig.server import WSGIServer

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

server = WSGIServer(app=app, host='localhost', port=8000)
server.serve_forever()

```

### Docker

Para crear una imagen de Docker para el servidor WSGI, sigue estos pasos:


Construye la imagen de Docker:

    ```bash
    docker build -t my-wsgi-server .
    ```

Ejecuta el contenedor de Docker:

    ```bash
    docker run -p 8081:8081 my-wsgi-server
    ```

El servidor se iniciará y escuchará en el puerto 8000. Puedes probar el servidor abriendo un navegador web y navegando a `http://localhost:8081`, `http://localhost:8081/html`, o `http://localhost:8081/json`. Deberías ver diferentes tipos de contenido mostrados en el navegador.
