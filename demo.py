import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import argparse
from DailyLogger.DailyLogger import DailyLogger

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("-f", "--folder",
						required=False,
						help="Name of the subfolder where log files would be stored",
						type=str)

arg_parser.add_argument("-p", "--project",
						required=False,
						help="Project name, which would be used as logfile prefix",
						type=str)

arg_parser.add_argument("-l", "--level",
						required=False,
						help="Level for logging",
						choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'],
						type=str)

arg_parser.add_argument("-o", "--output",
						required=False,
						help="Flag to decide whether or not display to stdout",
						action='store_true')

args = vars(arg_parser.parse_args())

py_logger = DailyLogger(
	log_folder=args['folder'],
	project_name=args['project'],
	log_level=args['level'],
	should_also_log_to_stdout=args['output']
)
logger = py_logger.get_logger()


@py_logger.log_function_call
def demo_function(arg_1=None, arg_2=None, *args, **kwargs):
	pass


@py_logger.log_function_call
def main():
	logger.info(py_logger.as_header_style('START: DEMO LOGGING'))

	demo_function(
		1, 2, 3,
		kwarg_1='Demo value 1',
		kwarg_2='Demo value 2'
	)

	logger.info('Testing 1 2 3 ...')

	try:
		raise Exception('An error was forced.')
	except Exception as err:
		logger.error(err)
		pass

	logger.info(DailyLogger.as_header_style('END: DEMO LOGGING'))

	return


if __name__ == '__main__':
	main()
