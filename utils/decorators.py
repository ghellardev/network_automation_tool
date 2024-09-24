# utils/decorators.py

# Import 'logging' module for logging
import logging
# Import 'wraps' to preserve function metadata
from functools import wraps


def log_decorator(func):
    """
    Decorator to log function calls and exceptions.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Log the function execution
        logging.info(f"Executing {func.__module__}.{func.__name__}")
        try:
            # Execute the original function
            return func(*args, **kwargs)
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error in {func.__module__}.{func.__name__}: {e}")
            # Re-raise the exception
            raise e

    # Return the wrapped function
    return wrapper
