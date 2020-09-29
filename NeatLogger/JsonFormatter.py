from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(
            json_ensure_ascii=False,
            reserved_attrs=[
                "args",
                "created",
                "exc_info",
                "exc_text",
                "levelno",
                "msecs",
                "msg",
                "relativeCreated",
                "stack_info",
            ],
            timestamp=True,
        )
