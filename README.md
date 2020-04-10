# NeatLogger
Convenient wrapper for logging python applications into files with desired separation intervals.

*Note*: Methods to initialize and terminate logging during `multiprocessing` is referenced from [multiprocessing-logging](https://github.com/jruere/multiprocessing-logging).


## Requirements

* Python 3+ (Tested in 3.7)
* multiprocessing-logging == 0.3.1


## Install with pip
```bash
$ pip install NeatLogger
```

## Usage
1. Import the library.
    ```python
    from NeatLogger import NeatLogger
    ```
2. Create an instance by defining the folder to store log files, the project name, the level of logging, the log file separation interval, whether to log to *sys.stdout* and whether to use UTC for logging.
    ```python
    NL = NeatLogger(
       project_name="demo",
       log_folder="demo_logs",
       log_level="info",
       log_to_stdout=True,
       use_utc = True,
       log_file_separation_interval="daily",
    )
    ```
3. Get a logger and start logging.
    ```python
    logger = NL.get_logger()
    logger.info("Testing 1 2 3 ...")
    ```

*"Testing 1 2 3 ..."* is logged to *sys.stdout*, as well as to *./demo_logs/demo_<`datetime`>.log*.

Sample usage is also available as **demo.py**. Please refer to it's help for more info.

For help:
```bash
python3 demo.py -h
```

To recreate Steps 1-3:
```bash
python3 demo.py -p demo -f demo_logs -i daily -l debug -o -u
```

## Author

**&copy; 2020, [Samyak Ratna Tamrakar](https://www.linkedin.com/in/srtamrakar/)**.