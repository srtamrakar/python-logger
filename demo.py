import asyncio
import time
from multiprocessing.pool import ThreadPool

from NeatLogger import Log
from NeatLogger.Formatter.configs import DEFAULT_IGNORE_ATTRIBUTE_LIST

ignore_log_attribute_list = DEFAULT_IGNORE_ATTRIBUTE_LIST.copy()
ignore_log_attribute_list.remove("threadName")
ignore_log_attribute_list.append("name")
NL = Log(
    project_name="demo",
    log_to_stdout=True,
    formatter="apache",
    ignore_log_attribute_list=ignore_log_attribute_list,
)
logger = NL.get_logger()


event_loop = asyncio.get_event_loop()


def pool_log_number(number: int):
    time.sleep(0.25)
    logger.info(f"Pool logging: {number}")


@NL.log_function_call
def demo_function(arg_1=None, arg_2=None, *args, **kwargs):
    pass


async def square(number: int) -> int:
    logger.info(f"Async calculating square of {number} ...")
    number_squared = number ** 2
    await asyncio.sleep(number_squared)
    logger.info(f"{number}^2 = {number_squared}")
    return number_squared


async def async_function(number: int):
    task_list = list()
    for i in reversed(range(number)):
        task_list.append(event_loop.create_task(square(i)))
    await asyncio.wait(task_list)


def main():
    logger.info("START")

    demo_function(1, 2, 3, kwarg_1="Demo value 1", kwarg_2="Demo value 2")
    logger.info("Logging umlauts: ä ö ü ß")

    NL.start_mp(logger)
    with ThreadPool(processes=3) as pool:
        pool.map(pool_log_number, range(6))
    NL.end_mp(logger)

    try:
        event_loop.run_until_complete(async_function(number=3))
    except Exception as err:
        logger.exception(err)
    finally:
        event_loop.close()

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
