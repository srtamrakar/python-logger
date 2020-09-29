import logging
from datetime import datetime


class ApacheFormatter(logging.Formatter):
    converter = datetime.fromtimestamp
    default_format = (
        "[timestamp %(asctime)s] [name %(name)s] [levelname %(levelname)s] "
        + "[pathname %(pathname)s] [filename %(filename)s] "
        + "[module %(module)s] [lineno %(lineno)d] [func %(funcName)s] "
        + "[thread %(thread)d] [threadName %(threadName)s] "
        + "[process %(process)d] [processName %(processName)s] "
        + "%(message)s"
    )

    def __init__(self, fmt=None, datefmt=None, style="%"):
        log_format = fmt if fmt is not None else self.default_format
        super().__init__(fmt=log_format, datefmt=datefmt, style=style)

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt is not None:
            s = ct.strftime(datefmt)
        else:
            s = datetime.fromtimestamp(
                record.created, tz=datetime.now().astimezone().tzinfo
            )
        return s
