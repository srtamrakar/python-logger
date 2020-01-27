import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import inspect
import time
import logging
from typing import NoReturn


class DailyLogger(object):
    """
    A basic daily logger to log python projects.

    ...

    Attributes
    ----------
    log_folder : str
        a folder
    project_name : str
        project name, which is used as suffix for the log file name
    log_level : str
        level for logging
    should_also_log_to_stdout : bool
        if True, also prints log to stdout

    Methods
    -------
    get_valid_logger()
        Returns a logger object.

    log_function_call()
        A wrapper that logs function call.
    """

    def __init__(
        self,
        log_folder: str = None,
        project_name: str = None,
        log_level: str = None,
        should_also_log_to_stdout: bool = True,
    ) -> NoReturn:
        """
        Parameters
        ----------
        log_folder : str, optional
            a folder
        project_name : str, optional
            project name, which is used as suffix for the log file name
        log_level : str, optional
            level for logging
        should_also_log_to_stdout : bool, optional
            if True, also prints log to stdout
        """

        if log_folder is None:
            log_folder = "logs"

        if project_name is None:
            project_name = "log"

        if log_level is None:
            log_level = "info"

        self.log_path = os.path.abspath(log_folder)
        self.project = project_name.lower()
        self.log_level = log_level.upper()
        self.should_also_log_to_stdout = should_also_log_to_stdout
        self.__initiate_path()
        self.__set_log_filename()
        self.__set_log_handlers()

    def __initiate_path(self) -> NoReturn:
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

    def __set_log_filename(self) -> NoReturn:
        today_date_str = time.strftime("%Y-%m-%d")
        self.log_filename = "{0}_{1}.{2}".format(self.project, today_date_str, "log")
        self.log_filepath = os.path.join(self.log_path, self.log_filename)

    def __set_log_handlers(self) -> NoReturn:
        self.log_handlers = [logging.FileHandler(self.log_filepath, encoding="utf-8")]
        if self.should_also_log_to_stdout:
            self.log_handlers.append(logging.StreamHandler(sys.stdout))

    def get_logger(self) -> logging.Logger:
        """
        Returns a logger object.
        """
        logging.basicConfig(
            handlers=self.log_handlers,
            level=self.log_level,
            format="%(asctime)-23.23s - %(levelname)-12.12s - F %(filename)-20.20s - L %(lineno)-4.4d :: %(message)s",
        )
        logger = logging.getLogger()
        return logger

    def log_function_call(self, func):
        """
        A wrapper that logs function call.
        """

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
    def as_header_style(cls, content: str = None) -> str:
        """
        Returns a text in header format.

        Parameters
        ----------
        content : str
            Any text.

        Returns
        -------
        str
            header format of a string for logging.
        """
        return "{:#^50s}".format(" {0} ".format(content))
