import os
import time
import datetime
import inspect
import pyfiglet
import logging
from typing import NoReturn
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from multiprocessing_logging import install_mp_handler, uninstall_mp_handler


from NeatLogger.exceptions import InvalidValue


class NeatLogger(object):
    def __init__(
        self,
        project_name: str = "log",
        log_folder: str = "logs",
        log_level: str = "info",
        log_file_suffix: str = "S",
        log_to_stdout: bool = True,
        log_to_file: bool = False,
        rotate_file_by_size: bool = False,
        rotating_file_max_size_bytes: int = 1048576,
        rotate_file_by_time: bool = False,
        rotation_period: str = "H",
        rotation_interval: int = 1,
        rotation_time: datetime.time = None,
        rotating_file_backup_count: int = 10,
        use_utc: bool = False,
        log_formatter: logging.Formatter = None,
    ) -> NoReturn:

        self.project = project_name
        self.log_folder = os.path.abspath(log_folder)
        self.log_level = log_level.upper()
        self.log_file_suffix = log_file_suffix
        self.log_to_stdout = log_to_stdout
        self.log_to_file = log_to_file
        self.rotate_file_by_size = rotate_file_by_size
        self.rotating_file_max_size_bytes = rotating_file_max_size_bytes
        self.rotate_file_by_time = rotate_file_by_time
        self.rotation_period = rotation_period.upper()
        self.rotation_interval = rotation_interval
        self.rotation_time = rotation_time
        self.rotating_file_backup_count = rotating_file_backup_count
        self.use_utc = use_utc
        self.__set_formatter(log_formatter)
        self.__set_logger()
        self.__set_log_handlers()
        self.__log_project_name()

    def __set_formatter(self, log_formatter: logging.Formatter = None) -> NoReturn:

        if log_formatter is not None:
            self.log_format = log_formatter
        else:
            self.log_format = logging.Formatter(
                fmt="%(asctime)-23.23s - %(levelname)-12.12s - "
                + "F %(filename)-20.20s - L %(lineno)-5.5d :: %(message)s",
            )
        if self.use_utc is True:
            self.log_format.converter = time.gmtime

    def __set_logger(self) -> NoReturn:
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)

    def get_logger(self) -> logging.Logger:
        return self.logger

    def __set_log_handlers(self) -> NoReturn:
        if self.rotate_file_by_size is True:
            self.__set_log_filepath(set_suffix=True)
            fh = RotatingFileHandler(
                filename=self.log_filepath,
                encoding="utf-8",
                maxBytes=self.rotating_file_max_size_bytes,
                backupCount=self.rotating_file_backup_count,
            )
            self.__add_handler(fh)

        elif self.rotate_file_by_time is True:
            self.__validate_rotation_period()
            self.__set_log_filepath(set_suffix=False)
            fh = TimedRotatingFileHandler(
                filename=self.log_filepath,
                encoding="utf-8",
                when=self.rotation_period,
                interval=self.rotation_interval,
                backupCount=self.rotating_file_backup_count,
                utc=self.use_utc,
                atTime=self.rotation_time,
            )
            self.__add_handler(fh)

        elif self.log_to_file is True:
            self.__set_log_filepath(set_suffix=True)
            fh = logging.FileHandler(filename=self.log_filepath, encoding="utf-8")
            self.__add_handler(fh)

        else:
            pass

        if self.log_to_stdout is True:
            sh = logging.StreamHandler()
            self.__add_handler(sh)

    def __set_log_filepath(self, set_suffix: bool = False) -> NoReturn:
        self.__set_log_filename(set_suffix=set_suffix)
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        self.log_filepath = os.path.join(self.log_folder, self.log_filename)

    def __validate_rotation_period(self) -> NoReturn:
        allowed_rotation_period_list = ["S", "H", "M", "D", "MIDNIGHT"]
        allowed_rotation_period_list += list(map(lambda n: f"W{n}", range(0, 7)))
        if self.rotation_period not in allowed_rotation_period_list:
            raise InvalidValue(
                self.rotation_period, allowed_rotation_period_list,
            )

    def __set_log_filename(self, set_suffix: bool = False) -> NoReturn:
        if set_suffix is True:
            self.log_filename = "{0}_{1}.{2}".format(
                self.project, self.__get_log_filename_suffix(), "log"
            )
        else:
            self.log_filename = f"{self.project}.log"

    def __get_log_filename_suffix(self) -> str:
        suffix_to_date_time_format_dict = {
            "D": "%Y-%m-%d",
            "H": "%Y-%m-%d__%H-00-00",
            "M": "%Y-%m-%d__%H-%M-00",
            "S": "%Y-%m-%d__%H-%M-%S",
        }

        if self.log_file_suffix not in suffix_to_date_time_format_dict.keys():
            raise InvalidValue(
                self.log_file_suffix, list(suffix_to_date_time_format_dict.keys())
            )
        datetime_now = self.__get_datetime_now()

        return datetime_now.strftime(
            suffix_to_date_time_format_dict[self.log_file_suffix]
        )

    def __get_datetime_now(self) -> datetime.datetime:
        if self.use_utc is True:
            return datetime.datetime.utcnow()
        else:
            return datetime.datetime.now()

    def __add_handler(self, handler: logging.Handler) -> NoReturn:
        handler.setLevel(self.log_level)
        handler.setFormatter(self.log_format)
        self.logger.addHandler(handler)

    def __log_project_name(self) -> NoReturn:
        ascii_text = pyfiglet.figlet_format(self.project, font="standard")
        self.logger.info(f"\n{ascii_text}")

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
