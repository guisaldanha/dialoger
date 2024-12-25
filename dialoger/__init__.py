from dialoger.options import options
from dialoger.input import input


def ask(title:str, question:str, answer_type:str, answer_default:str = None, pattern:str = None, allow_empty:bool = True, allow_cancel:bool = True) -> str:
    """
    Create an input window

    Args:
        title (str): window title
        question (str): question to be asked
        answer_type (str): type of answer (int, float, alphanumeric, str)
        allow_empty (bool, optional): allow empty answer. Defaults to True.
        answer_default (str, optional): default answer. Defaults to None.

    Returns:
        str: answer
    """
    answer = input(title=title, question=question, answer_type=answer_type, answer_default=answer_default, pattern=pattern, allow_empty=allow_empty, allow_cancel=allow_cancel, icon="question").get_answer()
    input._instance = None
    return answer


def askwithanswers(title:str, question:str, choices:list) -> str:
    """
    Create an window with a list of choices

    Args:
        title (str): window title
        question (str): question to be asked
        choices (list): list of choices

    Returns:
        str: choice
    """
    choice = options(title=title, message=question, choices=choices, icon="question").choice
    options._instance = None
    return choice


def confirm(title:str, message:str, choices:list=["Yes", "No"]) -> bool:
    """
    Create an confirmation window, with 2 choices, True is returned if the first choice is selected, False otherwise

    Args:
        title (str): window title
        message (str): message to be shown
        choices (list, optional): list of choices. Defaults to ["Yes", "No"]
    """
    assert len(choices) == 2, "The list of options must contain exactly two options."
    assert isinstance(choices[0], str) and isinstance(choices[1], str), "Options must be strings."
    choice = options(title=title, message=message, choices=choices, icon="question").choice
    options._instance = None
    return choice == choices[0]


def alert(title:str, message:str) -> str:
    """
    Create an alert window

    Args:
        title (str): window title
        message (str): message to be shown
    """
    options(title=title, message=message, choices=["OK"], icon="alert")
    options._instance = None
    return None


def info(title:str, message:str) -> str:
    """
    Create an information window

    Args:
        title (str): window title
        message (str): message to be shown
    """
    options(title=title, message=message, choices=["OK"], icon="info")
    options._instance = None
    return None


def error(title:str, message:str) -> str:
    """
    Create an error window

    Args:
        title (str): window title
        message (str): message to be shown
    """
    options(title=title, message=message, choices=["OK"], icon="error")
    options._instance = None
    return None


def success(title:str, message:str) -> str:
    """
    Create an success window

    Args:
        title (str): window title
        message (str): message to be shown
    """
    options(title=title, message=message, choices=["OK"], icon="success")
    options._instance = None
    return None
