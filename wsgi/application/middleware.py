"""Middlewares for the application."""

import time

def timing_middleware(func):
    """Middleware to print the time taken for each request."""
    def wrapper(request):
        start = time.time()
        response = func(request)
        end = time.time()
        print(f"Request took {end - start} seconds.")
        return response
    return wrapper


# class TimingMiddleware(object):
#     """Middleware to print the time taken for each request."""

#     def __init__(self, func):
#         self.func = func

#     def __call__(self, request):
#         start = time.time()
#         response = self.func(request)
#         end = time.time()
#         print(f"Request took {end - start} seconds.")
#         return response
