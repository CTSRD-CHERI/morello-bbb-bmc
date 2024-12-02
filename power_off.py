import logging
import os

from mcc import MCC


import pexpect


logging.basicConfig(level=os.getenv("LOGLEVEL", "WARNING").upper())
logger = logging.getLogger(__name__)


def main():
    with MCC() as mcc:
        mcc.to_state(MCC.CMD)
        mcc.ex.send("shutdown\n")
        idx = mcc.ex.expect(["Powering down...", pexpect.TIMEOUT], timeout=1)
        if idx == 0:
            print("System powering down")
        else:
            print("Error stopping system")
        idx = mcc.ex.expect(["Cmd>", pexpect.TIMEOUT], timeout=60)
        if idx == 0:
            print("System power down complete")
        else:
            print("System power down failed")

if __name__ == "__main__":
    main()
