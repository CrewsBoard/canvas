import os
import re


def get_root_path() -> str:
    """
    Get the root path of the project.

    Returns:
        str: The root path of the project.
    """
    current_file_path = os.path.abspath(__file__).split('src')
    current_file_path = current_file_path[:-1][0]
    return current_file_path


def get_project_name() -> str:
    """
    Get the project name.

    Returns:
        str: The project name.
    """
    root_path = get_root_path()
    project_name = root_path.split('/')[-2]
    return project_name


def make_snake_case(string: str) -> str:
    """
    Convert a string to snake_case.

    Args:
        string (str): The input string.

    Returns:
        str: The converted string in snake_case.
    """
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', string).lower()
