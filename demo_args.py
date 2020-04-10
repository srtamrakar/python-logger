import argparse

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument(
    "-f",
    "--folder",
    required=False,
    help="Name of the subfolder where log files would be stored.",
    type=str,
)

arg_parser.add_argument(
    "-p",
    "--project",
    required=False,
    help="Project name, which would be used as logfile prefix.",
    type=str,
)

arg_parser.add_argument(
    "-l",
    "--level",
    required=False,
    help="Level for logging.",
    choices=["critical", "error", "warning", "info", "debug", "notset"],
    type=str,
)

arg_parser.add_argument(
    "-i",
    "--separation-interval",
    required=False,
    help="Log separation interval.",
    choices=["daily", "hourly", "secondly"],
    type=str,
)

arg_parser.add_argument(
    "-u",
    "--use-utc",
    required=False,
    help="Flag to decide whether or not use UTC.",
    action="store_true",
)

arg_parser.add_argument(
    "-o",
    "--output",
    required=False,
    help="Flag to decide whether or not display to stdout.",
    action="store_true",
)


def get() -> dict:
    args = vars(arg_parser.parse_args())

    return args
