# DailyLogger
A basic daily logger to log python projects.

## Requirements

* Python 3+ (Tested in 3.7)

## Install with pip
```bash
$ pip install DailyLogger
```

## Usage
1. Import the library.
```python
from DailyLogger import DailyLogger
```

1. Create an instance by defining the path for logfiles, the project name, the level of logging
and whether to log to *sys.stdout*.
```python
py_logger = DailyLogger(log_subfolder='demo_logs', project_name='demo', log_level='info', should_also_log_to_stdout=True)
```

1. Get valid logger and start logging.
```python
logger = py_logger.get_logger()
logger.info('Testing 1 2 3 ...')
```

*"Testing 1 2 3 ..."* is logged to *sys.stdout*, as well as to *./demo_logs/demo_<YYYY-MM-DD>.log*.

Sample usage is also available as **demo.py**. Please refer to it's help for more info.

For help:
```bash
python3 demo.py -h
```

To recreate Steps 1-3:
```bash
python3 demo.py -p demo -f demo_logs -l info -o
```

## Author

* **&copy; Samyak Ratna Tamrakar** - [Github](https://github.com/srtamrakar), [LinkedIn](https://www.linkedin.com/in/srtamrakar/).