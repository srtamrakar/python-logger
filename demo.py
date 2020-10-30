import time
from multiprocessing.pool import ThreadPool
from NeatLogger import Log

NL = Log(
    project_name="demo",
    assign_logger_name=True,
    log_to_stdout=True,
    formatter="apache",
)
logger = NL.get_logger()


def log_number(number: int):
    time.sleep(0.25)
    logger.info(f"Logging: {number}")


@NL.log_function_call
def demo_function(arg_1=None, arg_2=None, *args, **kwargs):
    pass


def main():
    logger.info("START")

    demo_function(1, 2, 3, kwarg_1="Demo value 1", kwarg_2="Demo value 2")
    logger.info("Logging umlauts: ä ö ü ß")

    NL.start_mp(logger)
    with ThreadPool(processes=3) as pool:
        pool.map(log_number, range(10))
    NL.end_mp(logger)

    logger.warning("Warning!")
    logger.debug("Debugging ...")

    try:
        raise Exception("An error was forced.")
    except Exception as err:
        logger.exception(err)
        pass

    logger.info("END")

    return


if __name__ == "__main__":
    main()
