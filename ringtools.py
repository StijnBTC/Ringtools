import argparse
import sys

from lnd import Lnd
from output import Output
from status import Status


class RingTools:
    def __init__(self, arguments):
        self.lnd = Lnd(arguments.lnddir, arguments.grpc)
        self.output = Output(self.lnd)
        self.arguments = arguments

    def start(self):
        print(self.arguments.function)
        if self.arguments.function == "status":
            Status(self.lnd, self.output, self.arguments.channels_file, self.arguments.loop).run()
        pass


def main():
    argument_parser = get_argument_parser()
    arguments = argument_parser.parse_args()
    return RingTools(arguments).start()


def get_argument_parser():
    parser = argparse.ArgumentParser()
    # This is needed for the cert and macaroon of LND
    parser.add_argument(
        "--lnddir",
        default="~/.lnd",
        dest="lnddir",
        help="(default ~/.lnd) lnd directory",
    )
    parser.add_argument(
        "--grpc",
        default="localhost:10009",
        dest="grpc",
        help="(default localhost:10009) lnd gRPC endpoint",
    )
    parser.add_argument(dest="function", choices=['status'])
    status_group = parser.add_argument_group(
        "status",
        "Get the current status of all channels",
    )
    status_group.add_argument(
        "-channels-file",
        "-f",
        default="./channels.txt",
        dest="channels_file",
        help="(default ./channels.txt) channels file"
    )
    status_group.add_argument(
        "-l",
        "--loop",
        action="store_true",
        dest="loop",
        help="(default False) Keeps checking channel status"
    )
    return parser


success = main()
if success:
    sys.exit(0)
sys.exit(1)
