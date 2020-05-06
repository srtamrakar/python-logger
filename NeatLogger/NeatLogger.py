import os
import inspect
import logging
import time
from datetime import datetime
from typing import NoReturn
from multiprocessing_logging import install_mp_handler, uninstall_mp_handler
from NeatLogger.exceptions import InvalidValue


class NeatLogger(object):
    def __init__(
        self,
        project_name: str = "log",
        log_folder: str = "logs",
        log_level: str = "info",
        log_file_separation_interval: str = "secondly",
        log_to_stdout: bool = True,
        use_utc: bool = False,
    ) -> NoReturn:

        self.project = project_name.lower()
        self.log_folder = os.path.abspath(log_folder)
        self.log_level = log_level.upper()
        self.log_to_stdout = log_to_stdout
        self.use_utc = use_utc
        self.__set_log_file_separation_interval(log_file_separation_interval)
        self.__set_log_filename()
        self.__set_log_filepath()
        self.__set_formatter()
        self.__set_logger()
        self.__set_log_handlers()

    def __set_log_file_separation_interval(
        self, log_file_separation_interval: str
    ) -> NoReturn:
        log_file_separation_interval = log_file_separation_interval.lower()
        allowed_value_list = ["daily", "hourly", "secondly"]

        if log_file_separation_interval not in allowed_value_list:
            raise InvalidValue(log_file_separation_interval, allowed_value_list)

        self.log_file_separation_interval = log_file_separation_interval

    def __get_datetime_now(self) -> datetime:
        if self.use_utc is True:
            return datetime.utcnow()
        else:
            return datetime.now()

    def __get_log_filename_suffix(self) -> str:
        datetime_now = self.__get_datetime_now()

        separation_interval_to_format_dict = {
            "daily": "%Y-%m-%d",
            "hourly": "%Y-%m-%d__%H-00-00",
            "secondly": "%Y-%m-%d__%H-%M-%S",
        }

        return datetime_now.strftime(
            separation_interval_to_format_dict[self.log_file_separation_interval]
        )

    def __set_log_filename(self) -> NoReturn:
        self.log_filename = "{0}_{1}.{2}".format(
            self.project, self.__get_log_filename_suffix(), "log"
        )

    def __set_log_filepath(self) -> NoReturn:
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        self.log_filepath = os.path.join(self.log_folder, self.log_filename)

    def __set_formatter(self) -> NoReturn:
        self.log_format = logging.Formatter(
            fmt="%(asctime)-23.23s - %(levelname)-12.12s - "
            + "F %(filename)-20.20s - L %(lineno)-4.4d :: %(message)s",
        )
        if self.use_utc is True:
            self.log_format.converter = time.gmtime

    def __set_logger(self) -> NoReturn:
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)

    def __add_handler(self, handler: logging.Handler) -> NoReturn:
        handler.setLevel(self.log_level)
        handler.setFormatter(self.log_format)
        self.logger.addHandler(handler)

    def __set_log_handlers(self) -> NoReturn:
        fh = logging.FileHandler(self.log_filepath, encoding="utf-8")
        self.__add_handler(fh)

        if self.log_to_stdout is True:
            sh = logging.StreamHandler()
            self.__add_handler(sh)

    def log_function_call(self, func):
        def wrapper(*args, **kwargs):
            func_args = inspect.signature(func).bind(*args, **kwargs).arguments
            self.get_logger().info(
                "{0}.{1}({2})".format(
                    func.__module__,
                    func.__qualname__,
                    ", ".join("{} = {!r}".format(*item) for item in func_args.items()),
                )
            )
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def as_header_style(cls, content: str) -> str:
        return "{:#^50s}".format(" {0} ".format(content))

    @classmethod
    def start_mp(cls, logger: logging.Logger) -> NoReturn:
        install_mp_handler(logger)

    @classmethod
    def end_mp(cls, logger: logging.Logger) -> NoReturn:
        uninstall_mp_handler(logger)

    def get_logger(self) -> logging.Logger:
        return self.logger
