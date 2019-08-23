import logging
from datetime import datetime, timezone

from . import configs, utils


class Apache(logging.Formatter):
    converter = datetime.fromtimestamp

    def __init__(self, fmt=None, datefmt=None, style="%", *args, **kwargs):

        self.use_utc = kwargs.pop("use_utc", False)
        self.add_colors = kwargs.pop("add_colors", False)
        self.ignore_log_attribute_list = kwargs.pop("ignore_log_attribute_list", None)
        self.timezone = (
            timezone.utc if self.use_utc is True else datetime.now().astimezone().tzinfo
        )

        if self.ignore_log_attribute_list is None:
            self.ignore_log_attribute_list = configs.DEFAULT_IGNORE_ATTRIBUTE_LIST

        if fmt is not None:
            log_format = fmt
        else:
            log_format = utils.get_apache_log_format(
                attr_config_dict=configs.LOG_ATTRIBUTES_TO_NAME_AND_FORMAT_AND_COLOR_DICT,
                ignore_attr_list=self.ignore_log_attribute_list,
                add_colors=self.add_colors,
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
