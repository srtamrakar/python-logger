# NeatLogger
Convenient wrapper for logging python applications into files with desired separation intervals.

*Note*: Methods to initialize and terminate logging during `multiprocessing` is referenced from [multiprocessing-logging](https://github.com/jruere/multiprocessing-logging).


## Install with pip
```bash
$ pip install NeatLogger
```

## Usage
1. Import the library.
    ```python
    from NeatLogger import Log
    ```

2. Create an instance.
    ```python
    log = Log()
    ```
    Arguments (all are optional):
    * `project_name`: Project name which would be used as log file's prefix.
    * `log_folder`: Folder where log files would be stored.
    * `log_level`: Level for logging. Choices:
        * `"critical"`
        * `"error"`
        * `"warning"`
        * `"info"`
        * `"debug"`
        * `"notset"`
    * `log_file_suffix`: Log file suffix. Ignored when files are rotated by time. Choices:
        * `"S"`: `%Y-%m-%d__%H-%M-%S` is appended to the filename.
        * `"M"`: `%Y-%m-%d__%H-%M-00` is appended to the filename.
        * `"H"`: `%Y-%m-%d__%H-00-00` is appended to the filename.
        * `"D"`: `%Y-%m-%d` is appended to the filename.
    * `log_to_stdout`: Flag to decide whether or not to display logs in stdout.
    * `log_to_file`: Flag to decide whether or not to store logs in file.
    * `rotate_file_by_size`: Flag to decide whether or not to rotate file by size.
    * `rotating_file_max_size_bytes`: Size (in bytes) threshold to rollover the log file.
    * `rotate_file_by_time`: Flag to decide whether or not to rotate file by time.
    * `rotation_period`: Rotation period for the log file. Choices:
        * `"S"`: log file rollovers every second. Ignores `rotation_time`.
        * `"M"`: log file rollovers every minute. Ignores `rotation_time`.
        * `"H"`: log file rollovers every hour. Ignores `rotation_time`.
        * `"D"`: log file rollovers every day. Ignores `rotation_time`.
        * `"MIDNIGHT"`: log file rollovers at midnight, or at `rotation_time` _if specified_.
        * `"W0"`: log file rollovers on weekday 0 i.e. Monday at `rotation_time` _if specified_.
        * `"W1"`
        * `"W2"`
        * `"W3"`
        * `"W4"`
        * `"W5"`
        * `"W6"`
    * `rotation_interval`: Intervals of rotation period to rollover the log file. Ignored if `rotation_time` is a weekday.
    * `rotation_time`: Time of the day to rollover the log file when `rotation_period` = `"MIDNIGHT"` or a weekday. Default = `00:00`.
    * `rotating_file_backup_count`: Number of old files to be retained.
    * `use_utc`: Flag to decide whether or not to use UTC.
    * `log_formatter`: Logging formatter.
    
    :warning: If more than 1 of the following are set to `True`, only one of them is implemented. Their priority follows the order:
    * `rotate_file_by_size`
    * `rotate_file_by_time`
    * `log_to_file`

3. Get a logger and start logging.
    ```python
    logger = log.get_logger()
    logger.info("Testing 1 2 3 ...")
    ```


## Author

**&copy; 2020, [Samyak Ratna Tamrakar](https://www.linkedin.com/in/srtamrakar/)**.