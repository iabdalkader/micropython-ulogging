# This file is part of micropython-ulogging module.
#
# The MIT License (MIT)
#
# Copyright (c) 2022 Ibrahim Abdelkader <iabdalkader@openmv.io>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import time

if hasattr(time, "strftime"):
    from time import strftime
else:
    from ulogging.ustrftime import strftime

NOTSET   = 0
DEBUG    = 10 
INFO     = 20
WARNING  = 30
ERROR    = 40
CRITICAL = 50

levelname = {
    NOTSET  : "NOTSET",
    DEBUG   : "DEBUG",
    INFO    : "INFO",
    WARNING : "WARNING",
    ERROR   : "ERROR",
    CRITICAL: "CRITICAL",
}

loggers = {}
default_fmt = "%(levelname)s:%(name)s:%(message)s"
default_datefmt = "%Y-%m-%d %H:%M:%S"

class Handler:
    def __init__(self, level=NOTSET):
        self.level = level
        self.formatter = None

    def close(self):
        pass

    def setLevel(self, level):
        self.level = level

    def setFormatter(self, formatter):
        self.formatter = formatter

    def format(self, record):
        return self.formatter.format(record)

class StreamHandler(Handler):
    def __init__(self, stream=sys.stderr):
        self.stream = stream
        self.terminator = "\n"

    def close(self):
        if hasattr(self.stream, "flush"):
            self.stream.flush()

    def emit(self, record):
        if (record.level >= self.level):
            self.stream.write(self.format(record) + self.terminator)

class FileHandler(StreamHandler):
    def __init__(self, filename, mode="a", encoding="UTF-8"):
        super().__init__(stream=open(filename, mode=mode, encoding=encoding))

    def close(self):
        super().close()
        self.stream.close()

class Record:
    def set(self, name, level, message):
        self.name = name
        self.level = level
        self.message = message
        self.ts = time.time()
        self.msecs = int((self.ts- int(self.ts)) * 1000)

class Formatter:
    def __init__(self, fmt=default_fmt, datefmt=default_datefmt):
        self.fmt = fmt
        self.datefmt = datefmt

    def formatTime(self, datefmt):
        return strftime(datefmt, time.localtime())

    def format(self, record):
        return self.fmt % {
            "name"      : record.name,
            "message"   : record.message,
            "msecs"     : record.msecs,
            "asctime"   : self.formatTime(self.datefmt),
            "levelname" : levelname[record.level] }

class Logger():
    def __init__(self, name):
        self.name = name
        self.level = NOTSET
        self.handlers = []
        self.record = Record()

    def setLevel(self, level):
        self.level = level
        
    def addHandler(self, handler):
        self.handlers.append(handler)

    def hasHandlers(self):
        return len(self.handlers) > 0

    def debug(self, message, *args, **kwargs):
        self.log(DEBUG, message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        self.log(INFO, message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        self.log(WARNING, message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        self.log(ERROR, message, *args, **kwargs)
    
    def critical(self, message, *args, **kwargs):
        self.log(CRITICAL, message, *args, **kwargs)

    def log(self, level, message, *args, **kwargs):
        if (level >= self.level):
            if args and isinstance(args[0], dict):
                    args = args[0]
            for h in self.handlers:
                self.record.set(self.name, level, message % args)
                h.emit(self.record)

def debug(message, *args, **kwargs):
    getLogger().log(DEBUG, message, *args, **kwargs)

def info(message, *args, **kwargs):
    getLogger().log(INFO, message, *args, **kwargs)

def warning(message, *args, **kwargs):
    getLogger().log(WARNING, message, *args, **kwargs)

def error(message, *args, **kwargs):
    getLogger().log(ERROR, message, *args, **kwargs)

def critical(message, *args, **kwargs):
    getLogger().log(CRITICAL, message, *args, **kwargs)

def shutdown():
    for k, logger in loggers.items():
        for h in logger.handlers:
            h.close()
        loggers.pop(logger, None)

def getLogger(name="root"):
    if name not in loggers:
        loggers[name] = Logger(name)
    return loggers[name]

def basicConfig(filename=None, filemode="a", format=default_fmt, datefmt=default_datefmt,
        level=WARNING, stream=sys.stderr, encoding="UTF-8", force=False):
    logger = getLogger()
    if force or not logger.handlers:
        for h in logger.handlers:
            h.close()

        if filename is None:
            handler = StreamHandler(stream)
        else:
            handler = FileHandler(filename, filemode, encoding)

        handler.setLevel(level)
        handler.setFormatter(Formatter(format, datefmt))
        
        logger.setLevel(level)
        logger.addHandler(handler)
