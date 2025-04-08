import functools
import logging
import os
from typing import Optional, Callable, Any


class Logger(logging.Logger):
    def __init__(self, name: str, env: Optional[str] = None):
        super().__init__(name)

        self.env = env or os.getenv("ENVIRONMENT", "dev")
        log_level = logging.DEBUG if self.env == "dev" else logging.INFO
        self.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        self.addHandler(console_handler)


def log_execution(start_msg: str = "", end_msg: str = "") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            args_str = ", ".join(repr(arg) for arg in args)
            kwargs_str = ", ".join(f"{key}={repr(value)}" for key, value in kwargs.items())
            all_args_str = ", ".join(filter(None, [args_str, kwargs_str]))

            start_message = f"Starting execution of function: {func.__name__}({all_args_str})"
            logger.debug(start_message)
            logger.info(start_msg)
            try:
                result = func(*args, **kwargs)
                end_message = f"Finished execution of function: {func.__name__}. Result: {repr(result)}"
                logger.debug(end_message)
                logger.info(end_msg)
                return result
            except Exception as e:
                error_message = f"Exception during execution of {func.__name__}: {e}"
                logger.error(error_message, exc_info=True)
                raise

        return wrapper

    return decorator


logger = Logger(__name__)
