import os
import re


def get_root_path() -> str:
    """
    Get the root path of the project based on the given module name.

    Returns:
        str: The root path of the project.
    """
    current_file_path = os.path.abspath(__file__).split(get_project_name())
    current_file_path = current_file_path[:-1][0]
    return os.path.join(current_file_path, get_project_name())


def get_project_name() -> str:
    """
    Get the project name based on the root path of the given module.

    Returns:
        str: The name of the project.
    """
    return "canvas"


def make_snake_case(string: str) -> str:
    """
    Convert a string to snake_case.

    Args:
        string (str): The input string.

    Returns:
        str: The converted string in snake_case.
    """
    return re.sub(r"([a-z])([A-Z])", r"\1_\2", string).lower()
