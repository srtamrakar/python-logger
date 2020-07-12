from multiprocessing import Pool
from NeatLogger import NeatLogger
import demo_args

ARGS = demo_args.get()

NL = NeatLogger(
    project_name=ARGS["project"],
    log_folder=ARGS["folder"],
    log_level=ARGS["level"],
    log_to_stdout=ARGS["stdout"],
    log_to_file=ARGS["fileout"],
    use_utc=ARGS["use_utc"],
    log_file_separation_interval=ARGS["separation_interval"],
)
logger = NL.get_logger()

demo_args.log_args()


def log_number(number: int):
    logger.info(f"Logging: {number}")


@NL.log_function_call
def demo_function(arg_1=None, arg_2=None, *args, **kwargs):
    pass


@NL.log_function_call
def main():
    logger.info(NL.as_header_style("START: DEMO LOGGING"))

    demo_function(1, 2, 3, kwarg_1="Demo value 1", kwarg_2="Demo value 2")

    logger.info("Testing 1 2 3 ...")
    logger.info("Umlauts: ä ö ü ß")

    # with Pool(processes=5) as pool:
    #     NL.start_mp(logger)
    #     pool.map(log_number, range(10))
    #     NL.end_mp(logger)

    logger.warning("Warning!")
    logger.debug("Debugging ...")

    try:
        raise Exception("An error was forced.")
    except Exception as err:
        logger.error(err)
        pass

    logger.info(NeatLogger.as_header_style("END: DEMO LOGGING"))

    return


if __name__ == "__main__":
    main()
