import logging
from datetime import datetime, timezone

from .configs import DEFAULT_APACHE_FORMAT


class Apache(logging.Formatter):
    converter = datetime.fromtimestamp

    def __init__(self, fmt=None, datefmt=None, style="%", *args, **kwargs):
        log_format = fmt if fmt is not None else DEFAULT_APACHE_FORMAT
        self.use_utc = kwargs.pop("use_utc", False)
        self.timezone = (
            timezone.utc if self.use_utc is True else datetime.now().astimezone().tzinfo
        )
        super().__init__(fmt=log_format, datefmt=datefmt, style=style)

    def formatTime(self, record, datefmt=None):
        """Override: logging.Formatter.formatTime"""
        ct = self.converter(record.created)
        if datefmt is not None:
            s = ct.strftime(datefmt)
        else:
            s = datetime.fromtimestamp(record.created, tz=self.timezone)
        return s
