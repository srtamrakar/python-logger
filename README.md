# NeatLogger
Convenient wrapper for logging python applications with options to add color, select logging style, rotate files by size and time, etc.


## Install with pip
```bash
$ pip install NeatLogger
```

## Usage
1. Import the library.
    ```python
    from NeatLogger import Log
    ```

1. Create an instance.
    ```python
    log = Log()
    ```
    Arguments (all are optional):
    * `project_name`: Project name, which would serve as the logger's name (_if specified_) and the prefix for log filenames.
    * `log_folder`: Folder where log files are stored.
    * `log_level`: Level for logging. Choices:
        * `"critical"`
        * `"error"`
        * `"warning"`
        * `"info"`
        * `"debug"`
        * `"notset"`
    * `log_file_suffix`: Suffix for log filenames. Ignored if `rotate_file_by_time=True` . Choices:
        * `"S"`: `%Y-%m-%d_%H-%M-%S` is appended to the filename.
        * `"M"`: `%Y-%m-%d_%H-%M-00`
        * `"H"`: `%Y-%m-%d_%H-00-00`
        * `"D"`: `%Y-%m-%d`
    * `log_to_stdout`: Flag to decide whether or not to display the logs in stdout.
    * `log_to_file`: Flag to decide whether or not to store the logs in file.
    * `rotate_file_by_size`: Flag to decide whether or not to rotate the log files by size.
    * `rotating_file_max_size_bytes`: Size (in bytes) threshold to rollover the log files.
    * `rotate_file_by_time`: Flag to decide whether or not to rotate the log files by time. Ignores `log_file_suffix`.
    * `rotation_period`: Rotation period for the log files. Choices:
        * `"S"`: log file rollovers every second. Ignores `rotation_time`.
        * `"M"`: log file rollovers every minute. Ignores `rotation_time`.
        * `"H"`: log file rollovers every hour. Ignores `rotation_time`.
        * `"D"`: log file rollovers every day. Ignores `rotation_time`.
        * `"MIDNIGHT"`: log file rollovers at midnight, or at `rotation_time` _if specified_.
        * `"W0"`: log file rollovers on weekday 0 i.e. Monday, at `rotation_time` _if specified_.
        * `"W1"`
        * `"W2"`
        * `"W3"`
        * `"W4"`
        * `"W5"`
        * `"W6"`
    * `rotation_interval`: Intervals of rotation period to rollover the log files. Ignored if `rotation_time` is a weekday.
    * `rotation_time`: Time of the day to rollover the log file when `rotation_period` = `"MIDNIGHT"` or a weekday.
    * `rotating_file_backup_count`: Number of old files to be retained.
    * `use_utc`: Flag to decide whether or not to use UTC in the log timestamp and filenames.
    * `assign_logger_name`: Flag to decide whether or not to assign `project_name` as the name to the logger.
    * `colors_to_stdout`: Flag to decide whether or not to have colorful log. Only works for `log_to_stdout=True` and `log_formatter="apache"`.
    * `formatter`: Logging formatter. Choices:
        * an instance of `logging.Formatter`
        * `"json"`
        * `"apache"`
    * `ignore_log_attribute_list`: List of log attributes to be ignored in log. By default, some of the attributes are ignored. If all the attributes are desired, use `ignore_log_attribute_list=list()`.

    :warning: If more than 1 of the following are set to `True`, only one of them is implemented. Their priority follows the order:
    1. `rotate_file_by_size`
    1. `rotate_file_by_time`
    1. `log_to_file`

1. Get a logger and start logging.
    ```python
    logger = log.get_logger()
    logger.info("Testing 1 2 3 ...")
    ```


## Author

**&copy; 2020, [Samyak Ratna Tamrakar](https://www.linkedin.com/in/srtamrakar/)**.