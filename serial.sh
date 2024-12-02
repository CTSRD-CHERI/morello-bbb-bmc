#! /bin/bash

exec picocom -n -q -b115200 --send-cmd='' --receive-cmd='' /dev/ttyUSB2
