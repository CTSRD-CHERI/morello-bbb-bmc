import logging

import serial
import pexpect
import pexpect.fdpexpect


logger = logging.getLogger(__name__)


class MCC(object):
    CMD = 0
    DEBUG = 1

    def __init__(self):
        self.state = None

    def __enter__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)
        self.ex = pexpect.fdpexpect.fdspawn(self.serial)
        self.ex.send("\n")
        self.determine_state()
        return self

    def __exit__(self, eType, value, traceback):
        self.serial.close()

    def determine_state(self):
        while True:
            idx = self.ex.expect_exact(["Cmd>", "Debug>", pexpect.TIMEOUT], timeout=1)
            if idx == 0:
                logger.info("state:CMD")
                self.state = MCC.CMD
                return
            elif idx == 1:
                logger.info("state:DEBUG")
                self.state = MCC.DEBUG
                return
            else:
                logger.info(self.ex.before)
                self.ex.send("\n")

    def to_state(self, state):
        logger.info(f"to_state({state})")
        while True:
            if self.state == state:
                return
            elif self.state == MCC.CMD and state == MCC.DEBUG:
                logger.info("cmd -> debug")
                self.ex.send("debug\n")
                self.determine_state()
            elif self.state == MCC.DEBUG and state == MCC.CMD:
                logger.info("debug -> cmd")
                self.ex.send("exit\n")
                self.determine_state()
            else:
                self.determine_state()
