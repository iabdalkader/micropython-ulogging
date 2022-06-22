## micropython-ulogging

A better MicroPython `ulogging` module, supports `datefmt` and `format` that actually work and Stream and File handlers. Note: Although not strictly necessary, it's recommended that the port/board enable `MICROPY_PY_SYS_ATEXIT` when using this module, to shutdown handlers at exit.

### Basic example:
```python
import ulogging

ulogging.basicConfig(
        level=ulogging.DEBUG,
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s")

ulogging.debug("This is a debug message.")
ulogging.info("This is an info message.")
ulogging.warning("This is a warning message.")
ulogging.error("This is an error message with non-ASCII stuff, like Øresund and Malmö")
```

Output:
```
03:18:52.000 - root - DEBUG - This is a debug message.
03:18:52.000 - root - INFO - This is an info message.
03:18:52.000 - root - WARNING - This is a warning message.
03:18:52.000 - root - ERROR - This is an error message with non-ASCII stuff, like Øresund and Malmö
```

### Advanced example:
```python
import ulogging

# Create logger
logger = ulogging.getLogger(__name__)
logger.setLevel(ulogging.DEBUG)

# Create console handler and set level to debug
stream_handler = ulogging.StreamHandler()
stream_handler.setLevel(ulogging.DEBUG)

# Create file handler and set level to error
file_handler = ulogging.FileHandler("error.log", mode="w")
file_handler.setLevel(ulogging.ERROR)

# Create a formatter
formatter = ulogging.Formatter("%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s")

# Add formatter to the handlers
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add stream_handler to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
```

Output:
```
2022-06-22 21:34:12.494 - __main__ - DEBUG - debug message
2022-06-22 21:34:12.494 - __main__ - INFO - info message
2022-06-22 21:34:12.494 - __main__ - WARNING - warn message
2022-06-22 21:34:12.495 - __main__ - ERROR - error message
2022-06-22 21:34:12.495 - __main__ - CRITICAL - critical message

$ cat errror.log
2022-06-22 21:34:12.495 - __main__ - ERROR - error message
2022-06-22 21:34:12.495 - __main__ - CRITICAL - critical message
```
