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
        output = ""
        while True:
            idx = mcc.ex.expect(["Debug>", pexpect.TIMEOUT], timeout=1)
            if idx == 0:
                output += str(mcc.ex.before)
                if "HELP or ?" in output:
                    board_power = ("VOLTS" in output)
                    print(f"{board_power}")
                    break
            else:
                print("ERROR")
                break

        mcc.to_state(MCC.CMD)


if __name__ == "__main__":
    main()
