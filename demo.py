import time
from multiprocessing import Pool
from NeatLogger import Log

NL = Log(
    project_name="demo",
    log_folder="demo_logs",
    log_level="info",
    log_file_suffix="S",
    log_to_stdout=True,
    log_to_file=False,
    rotate_file_by_size=False,
    rotating_file_max_size_bytes=512,
    rotate_file_by_time=False,
    rotation_period="S",
    rotation_interval=1,
    rotation_time=None,
    rotating_file_backup_count=100,
    use_utc=False,
    log_formatter="apache",
)
logger = NL.get_logger()


def log_number(number: int):
    logger.info(f"Logging: {number}")


@NL.log_function_call
def demo_function(arg_1=None, arg_2=None, *args, **kwargs):
    pass


def main():
    demo_function(1, 2, 3, kwarg_1="Demo value 1", kwarg_2="Demo value 2")

    logger.info("Testing 1 2 3 ...")
    logger.info("Umlauts: ä ö ü ß")

    with Pool(processes=5) as pool:
        NL.start_mp(logger)
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
        logger.error(err)
        pass

    return


if __name__ == "__main__":
    main()
