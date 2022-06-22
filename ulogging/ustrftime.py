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
import re

TS_YEAR=0
TS_MON=1
TS_MDAY=2
TS_HOUR=3
TS_MIN=4
TS_SEC=5
TS_WDAY=6
TS_YDAY=7
TS_ISDST=8

WDAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
     "Saturday", "Sunday"]
MDAY = ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"]

regex = re.compile(r"%(-?[a-zA-Z])")

def strftime(datefmt, ts):
    return regex.sub(r"%(\1)s", datefmt) % {
        "a" : WDAY[ts[TS_WDAY]][0:3],
        "A" : WDAY[ts[TS_WDAY]],
        "b" : MDAY[ts[TS_MON]][0:3],
        "B" : MDAY[ts[TS_MON]],
        "d" : f"{ts[TS_MDAY]:02d}",
        "H" : f"{ts[TS_HOUR]:02d}",
        "I" : f"{ts[TS_HOUR]%12:02d}",
        "j" : f"{ts[TS_YDAY]:03d}",
        "m" : f"{ts[TS_MON]:02d}",
        "M" : f"{ts[TS_MIN]:02d}",
        "P" : "AM" if ts[TS_HOUR] < 12 else "PM",
        "S" : f"{ts[TS_SEC]:02d}",
        "w" : f"{ts[TS_WDAY]}",
        "y" : f"{ts[TS_YEAR]%100:02d}",
        "Y" : f"{ts[TS_YEAR]}",
    }

if __name__ == "__main__":
    import time
    fmt = "%Y-%m-%d %a %b %I:%M:%S %P"
    print(strftime(fmt, time.localtime()))
