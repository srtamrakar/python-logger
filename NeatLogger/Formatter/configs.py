LOG_ATTRIBUTES_TO_STRING_FORMAT_DICT = {
    "args": None,
    "asctime": "s",
    "created": "f",
    "exc_info": None,
    "exc_text": None,
    "filename": "s",
    "funcName": "s",
    "levelname": "s",
    "levelno": "d",
    "lineno": "d",
    "message": "s",
    "module": "s",
    "msecs": "d",
    "msg": None,
    "name": "s",
    "pathname": "s",
    "process": "d",
    "processName": "s",
    "relativeCreated": "d",
    "stack_info": None,
    "thread": "d",
    "threadName": "s",
}

REMOVE_ATTRIBUTE_LIST = [
    "args",
    "created",
    "exc_info",
    "exc_text",
    "pathname",
    "levelno",
    "msecs",
    "msg",
    "relativeCreated",
    "stack_info",
]

DEFAULT_APACHE_FORMAT = ""
for attr, str_format in LOG_ATTRIBUTES_TO_STRING_FORMAT_DICT.items():
    if attr == "message" or attr in REMOVE_ATTRIBUTE_LIST:
        continue
    attr_name = "timestamp" if attr == "asctime" else attr
    DEFAULT_APACHE_FORMAT += f"[{attr_name} %({attr}){str_format}] "
DEFAULT_APACHE_FORMAT += "%(message)s"
