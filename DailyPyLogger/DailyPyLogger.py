import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import inspect
import time
import logging


class DailyPyLogger(object):
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
			log_folder=None,
			project_name=None,
			log_level=None,
			should_also_log_to_stdout=None
	):
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
		if should_also_log_to_stdout is None:
			should_also_log_to_stdout = True

		if log_folder is None:
			log_folder = 'logs'

		if project_name is None:
			project_name = 'log'

		if log_level is None:
			log_level = 'info'

		self.log_path = os.path.abspath(log_folder)
		self.project = project_name.lower()
		self.log_level = log_level.upper()
		self.should_also_log_to_stdout = should_also_log_to_stdout
		self.__initiate_path()
		self.__set_log_filename()
		self.__set_log_handlers()

	def __initiate_path(self):
		if not os.path.exists(self.log_path):
			os.makedirs(self.log_path)
		return

	def __set_log_filename(self):
		today_date_str = time.strftime("%Y-%m-%d")
		self.log_filename = '{0}_{1}.{2}'.format(self.project, today_date_str, 'log')
		self.log_filepath = os.path.join(self.log_path, self.log_filename)
		return

	def __set_log_handlers(self):
		self.log_handlers = [logging.FileHandler(self.log_filepath)]
		if self.should_also_log_to_stdout:
			self.log_handlers.append(logging.StreamHandler(sys.stdout))
		return

	def get_logger(self):
		"""
		Returns a logger object.
		"""
		logging.basicConfig(
			handlers=self.log_handlers,
			level=self.log_level,
			format='%(asctime)-23.23s - %(levelname)-5.5s - F %(filename)-20.20s - L %(lineno)-4.4d :: %(message)s'
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
				'{0}.{1}({2})'.format(
					func.__module__,
					func.__qualname__,
					', '.join('{} = {!r}'.format(*item) for item in func_args.items())
				)
			)

		return wrapper


	@classmethod
	def as_header_style(cls, content=None):
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
		return '{:#^50s}'.format(' {0} '.format(content))
