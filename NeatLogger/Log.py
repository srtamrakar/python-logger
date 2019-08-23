import datetime
import inspect
import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import List, NoReturn, Union

import pyfiglet
from multiprocessing_logging import install_mp_handler, uninstall_mp_handler

from .exceptions import InvalidValue
from .Formatter import Apache, Json


class Log(object):

    ALLOWED_FORMATTER_STR_LIST = ["json", "apache"]

    def __init__(
        self,
        project_name: str = "log",
        log_level: str = "info",
        assign_logger_name: bool = False,
        formatter: Union[str, logging.Formatter] = "apache",
        log_to_stdout: bool = True,
        log_to_file: bool = False,
        log_dir: str = "logs",
        log_file_suffix: str = "S",
        rotate_file_by_size: bool = False,
        rotating_file_max_size_bytes: int = 1048576,
        rotate_file_by_time: bool = False,
        rotation_period: str = "H",
        rotation_interval: int = 1,
        rotation_time: datetime.time = None,
        rotating_file_backup_count: int = 1024,
        use_utc: bool = False,
        colors_to_stdout: bool = True,
        ignore_log_attribute_list: List[str] = None,
    ) -> NoReturn:

        self.project_name = project_name
        self.log_level = log_level.upper()
        self.assign_logger_name = assign_logger_name
        self.input_formatter = formatter
        self.log_to_stdout = log_to_stdout
        self.log_to_file = log_to_file
        self.log_dir = os.path.abspath(log_dir)
        self.log_file_suffix = log_file_suffix
        self.rotate_file_by_size = rotate_file_by_size
        self.rotating_file_max_size_bytes = rotating_file_max_size_bytes
        self.rotate_file_by_time = rotate_file_by_time
        self.rotation_period = rotation_period.upper()
        self.rotation_interval = rotation_interval
        self.rotation_time = rotation_time
        self.rotating_file_backup_count = rotating_file_backup_count
        self.use_utc = use_utc
        self.colors_to_stdout = colors_to_stdout
        self.ignore_log_attribute_list = ignore_log_attribute_list
        self.__set_logger()
        self.__set_log_handlers()
        self.__print_project_name()

    def __set_logger(self) -> NoReturn:
        if self.assign_logger_name is True:
            self.__logger = logging.getLogger(name=self.project_name)
        else:
            self.__logger = logging.getLogger()

        self.__logger.setLevel(self.log_level)

    def get_logger(self) -> logging.Logger:
        return self.__logger

    def __set_log_handlers(self) -> NoReturn:
        if self.rotate_file_by_size is True:
            self.__set_log_filepath(set_suffix=True)
            fh = RotatingFileHandler(
                filename=self.__log_filepath,
                encoding="utf-8",
                maxBytes=self.rotating_file_max_size_bytes,
                backupCount=self.rotating_file_backup_count,
            )
            self.__add_handler(handler=fh, add_colors=False)

        elif self.rotate_file_by_time is True:
            self.__validate_rotation_period()
            self.__set_log_filepath(set_suffix=False)
            fh = TimedRotatingFileHandler(
                filename=self.__log_filepath,
                encoding="utf-8",
                when=self.rotation_period,
                interval=self.rotation_interval,
                backupCount=self.rotating_file_backup_count,
                utc=self.use_utc,
                atTime=self.rotation_time,
            )
            self.__add_handler(handler=fh, add_colors=False)

        elif self.log_to_file is True:
            self.__set_log_filepath(set_suffix=True)
            fh = logging.FileHandler(filename=self.__log_filepath, encoding="utf-8")
            self.__add_handler(handler=fh, add_colors=False)

        else:
            pass

        if self.log_to_stdout is True:
            sh = logging.StreamHandler()
            self.__add_handler(handler=sh, add_colors=self.colors_to_stdout)

    def __set_log_filepath(self, set_suffix: bool = False) -> NoReturn:
        self.__set_log_filename(set_suffix=set_suffix)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.__log_filepath = os.path.join(self.log_dir, self.__log_filename)

    def __validate_rotation_period(self) -> NoReturn:
        allowed_rotation_period_list = ["S", "M", "H", "D", "MIDNIGHT"]
        allowed_rotation_period_list += list(map(lambda n: f"W{n}", range(0, 7)))
        if self.rotation_period not in allowed_rotation_period_list:
            raise InvalidValue(
                self.rotation_period,
                allowed_rotation_period_list,
            )

    def __set_log_filename(self, set_suffix: bool = False) -> NoReturn:
        if set_suffix is True:
            self.__log_filename = "{0}_{1}.{2}".format(
                self.project_name, self.__get_log_filename_suffix(), "log"
            )
        else:
            self.__log_filename = f"{self.project_name}.log"

    def __get_log_filename_suffix(self) -> str:
        suffix_to_date_time_format_dict = {
            "S": "%Y-%m-%d_%H-%M-%S",
            "M": "%Y-%m-%d_%H-%M-00",
            "H": "%Y-%m-%d_%H-00-00",
            "D": "%Y-%m-%d",
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

    def __add_handler(self, handler: logging.Handler, add_colors: bool) -> NoReturn:
        handler.setLevel(self.log_level)
        handler.setFormatter(self.__get_formatter(add_colors=add_colors))
        self.__logger.addHandler(handler)

    def __get_formatter(self, add_colors: bool) -> logging.Formatter:
        if isinstance(self.input_formatter, logging.Formatter) is True:
            return self.input_formatter

        elif isinstance(self.input_formatter, str) is True:
            if self.input_formatter.lower() == "json":
                return Json(
                    use_utc=self.use_utc,
                    ignore_log_attribute_list=self.ignore_log_attribute_list,
                )
            elif self.input_formatter.lower() == "apache":
                return Apache(
                    use_utc=self.use_utc,
                    add_colors=add_colors,
                    ignore_log_attribute_list=self.ignore_log_attribute_list,
                )
            else:
                raise InvalidValue(
                    value=self.input_formatter,
                    allowed_value_list=self.ALLOWED_FORMATTER_STR_LIST,
                )
        else:
            raise TypeError("'formatter' must be of type 'logging.Formatter' or 'str'")

    def __print_project_name(self) -> NoReturn:
        ascii_text = pyfiglet.figlet_format(self.project_name, font="standard")
        print(f"\n{ascii_text}")

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
    def start_mp(cls, logger: logging.Logger) -> NoReturn:
        install_mp_handler(logger)

    @classmethod
    def end_mp(cls, logger: logging.Logger) -> NoReturn:
        uninstall_mp_handler(logger)
