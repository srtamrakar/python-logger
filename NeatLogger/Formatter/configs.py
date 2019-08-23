from colorama import Fore

LOG_ATTRIBUTES_TO_NAME_AND_FORMAT_AND_COLOR_DICT = {
    "asctime": ("timestamp", "s", Fore.YELLOW),
    "created": (None, "f", Fore.YELLOW),
    "msecs": (None, "d", Fore.YELLOW),
    "relativeCreated": (None, "d", Fore.YELLOW),
    "name": (None, "s", Fore.MAGENTA),
    "levelname": (None, "s", Fore.RED),
    "levelno": (None, "d", Fore.RED),
    "pathname": (None, "s", Fore.CYAN),
    "filename": (None, "s", Fore.CYAN),
    "lineno": (None, "d", Fore.CYAN),
    "module": (None, "s", Fore.BLUE),
    "funcName": (None, "s", Fore.BLUE),
    "process": (None, "d", Fore.LIGHTGREEN_EX),
    "processName": (None, "s", Fore.LIGHTGREEN_EX),
    "thread": (None, "d", Fore.LIGHTBLUE_EX),
    "threadName": (None, "s", Fore.LIGHTBLUE_EX),
    "exc_info": (None, None, Fore.BLACK),
    "exc_text": (None, None, Fore.BLACK),
    "stack_info": (None, None, Fore.BLACK),
    "args": (None, None, Fore.WHITE),
}
# "msg" and "message" are excluded on purpose

DEFAULT_IGNORE_ATTRIBUTE_LIST = [
    "args",
    "created",
    "exc_info",
    "exc_text",
    "pathname",
    "levelno",
    "msecs",
    "relativeCreated",
    "stack_info",
    "module",
    "funcName",
    "thread",
    "threadName",
    "process",
    "processName",
]
