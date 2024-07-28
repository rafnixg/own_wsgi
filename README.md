# Tutorial: Own WSGI Server.

This is a simple tutorial on how to create your own WSGI server. This tutorial is for educational purposes only. It is not recommended to use this server in production.

## What is WSGI?

WSGI stands for Web Server Gateway Interface. It is a specification that describes how a web server communicates with web applications. WSGI is a standard interface between web servers and Python web frameworks or applications. It allows you to write web applications independently of the web server.
PEP 3333 is the official specification for WSGI in Python. (https://www.python.org/dev/peps/pep-3333/)[https://www.python.org/dev/peps/pep-3333/]

## Parts of a WSGI Server

A WSGI server consists of two main parts:

1. Web Server: The web server is responsible for accepting incoming HTTP requests and passing them to the WSGI application.

2. WSGI Application: The WSGI application is a Python callable that takes two arguments: `environ` and `start_response`. The `environ` argument is a dictionary containing the HTTP request information, and the `start_response` argument is a callable that is used to send the HTTP response headers.

## Creating a Simple WSGI Server

Here is an example of a simple WSGI server that listens on port 8000 and responds with a "Hello, World!" message:

```python

import socket

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [b'Hello, World!']

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024)
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.input': data
        }
        response = application(environ, start_response)
        client_socket.sendall(b'HTTP/1.1 200 OK\r\n')
        client_socket.sendall(b'Content-Type: text/plain\r\n\r\n')
        client_socket.sendall(b'Hello, World!')
        client_socket.close()

if __name__ == '__main__':
    run_server()

```

To run the server, save the code to a file named `server.py` and run it using the following command:

```bash
python server.py
```

The server will start listening on port 8000. You can test the server by opening a web browser and navigating to `http://localhost:8000`. You should see a "Hello, World!" message displayed in the browser.


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
