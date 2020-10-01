import time
from multiprocessing.pool import ThreadPool
from NeatLogger import Log

NL = Log(
    project_name="demo",
    log_folder="logs",
    log_level="info",
    log_file_suffix="D",
    log_to_stdout=True,
    log_to_file=False,
    rotate_file_by_size=False,
    rotating_file_max_size_bytes=2048,
    rotate_file_by_time=False,
    rotation_period="S",
    rotation_interval=1,
    rotation_time=None,
    rotating_file_backup_count=100,
    use_utc=False,
    assign_logger_name=False,
    colors_to_stdout=True,
    formatter="json",
    ignore_log_attribute_list=[
        "args",
        "created",
        "exc_info",
        "exc_text",
        "pathname",
        "levelno",
        "msecs",
        "relativeCreated",
        "stack_info",
        "name",
        "levelname",
        "module",
        "funcName",
        "process",
        "processName",
        "thread",
    ],
)
logger = NL.get_logger()


def log_number(number: int):
    time.sleep(1)
    logger.info(f"Logging: {number}")


@NL.log_function_call
def demo_function(arg_1=None, arg_2=None, *args, **kwargs):
    pass


def main():
    logger.info("START")

    demo_function(1, 2, 3, kwarg_1="Demo value 1", kwarg_2="Demo value 2")
    logger.info("Logging umlauts: ä ö ü ß")

    NL.start_mp(logger)
    with ThreadPool(processes=10) as pool:
        pool.map(log_number, range(10))
    NL.end_mp(logger)

    logger.warning("Warning!")
    logger.debug("Debugging ...")

    for iteration_number in range(10):
        time.sleep(0.5)
        logger.info(f"iteration_number={iteration_number}")

    try:
        raise Exception("An error was forced.")
    except Exception as err:
        logger.exception(err)
        pass

    logger.info("END")

    return


if __name__ == "__main__":
    main()
