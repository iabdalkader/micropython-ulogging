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
from .ulogging import Logger
from .ulogging import Handler
from .ulogging import Formatter
from .ulogging import FileHandler
from .ulogging import StreamHandler
from .ulogging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from .ulogging import debug, info, warning, error, critical, exception
from .ulogging import shutdown
from .ulogging import getLogger
from .ulogging import basicConfig

try:
    import atexit
    atexit.register(shutdown)
except ImportError:
    import sys
    if hasattr(sys, "atexit"):
        sys.atexit(shutdown)
