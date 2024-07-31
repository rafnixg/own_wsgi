"""Utility functions for the server."""

import argparse


def get_directory_path():
    """Get the directory path from the command line arguments.
    args:
        --directory: str: The directory path.
    returns:
        str: The directory path.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="the directory path")
    args = parser.parse_args()
    if not args.directory:
        return None
    return args.directory


def print_welcome_message(app, host, port):
    """Print the welcome message."""
    print("Welcome the Simple WSGI Server!")
    print(f"Listening on {host}:{port}...\n")
    print("Press Ctrl+C to quit.\n")
    if app:
        print_avaliabe_endpoints(app)


def print_avaliabe_endpoints(app):
    """Print the available endpoints."""
    print("Available endpoints:")
    for path_operation in app.path_operations:
        print(f"[{path_operation.http_method}] {path_operation.path}")
