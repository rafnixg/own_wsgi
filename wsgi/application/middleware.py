"""Middlewares for the application."""

import time


def timing_middleware(func):
    """Middleware to print the time taken for each request.
    Args:
        func (callable): The function to call.
    Returns:
        callable: The wrapper function.
    """

    def wrapper(request):
        """Wrapper function for the middleware.
        Args:
            request (Request): The request.
        Returns:
            Response: The response.
        """
        start = time.time()
        response = func(request)
        end = time.time()
        print(f"Request took {end - start} seconds.")
        return response

    return wrapper
