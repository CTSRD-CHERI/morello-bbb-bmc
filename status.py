import logging
import os

from mcc import MCC


import pexpect


logging.basicConfig(level=os.getenv("LOGLEVEL", "WARNING").upper())
logger = logging.getLogger(__name__)


def main():
    with MCC() as mcc:
        mcc.to_state(MCC.DEBUG)
        mcc.ex.send("help\n")
        idx = mcc.ex.expect(["VOLTS", "Debug>", pexpect.TIMEOUT], timeout=1)
        board_power = (idx == 0)
        print(f"{board_power}")
        mcc.to_state(MCC.CMD)


if __name__ == "__main__":
    main()
