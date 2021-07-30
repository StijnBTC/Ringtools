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
        if self.arguments.function == "status":
            Status(self.lnd,
                   self.output,
                   self.arguments.channels_file,
                   self.arguments.loop,
                   self.arguments.show_fees).run()
        pass


def main():
    argument_parser = get_argument_parser()
    arguments = argument_parser.parse_args()
    return RingTools(arguments).start()


def get_argument_parser():
    parser = argparse.ArgumentParser()
    # This is needed for the cert and macaroon of LND
    parser.add_argument(
        dest="function",
        choices=['status'],
        help="Choose which function of the RingTools you would "
             "like to use",
        default="help",
    )
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
    status_group = parser.add_argument_group(
        "status",
        "Get the current status of all channels",
    )
    status_group.add_argument(
        "-channels-file",
        "-c",
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
    status_group.add_argument(
        '-f',
        '--show-fees',
        action="store_true",
        dest="show_fees",
        help="(default False) Shows fees in status screen"
    )
    return parser


success = main()
if success:
    sys.exit(0)
sys.exit(1)
