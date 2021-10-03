import argparse
import sys

from lnd import Lnd
from output import Output
from status import Status
from utils import is_umbrel
from checkring import CheckRing

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
        elif self.arguments.function == "check":
            CheckRing(self.lnd,
                   self.output,
                   self.arguments.pubkeys_file,
                   self.arguments.write_channels,
                   self.arguments.show_fees,
                   self.arguments.channels_file
                   ).run()
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
        choices=['status', 'check'],
        help="Choose which function of the RingTools you would "
             "like to use",
        default="help",
    )
    #If nodeos is Umbrel use the default umbrel lnd location
    lnd_dir = "~/.lnd"
    if is_umbrel():
        lnd_dir = "~/umbrel/lnd"

    parser.add_argument(
        "--lnddir",
        default=lnd_dir,
        dest="lnddir",
        help="(default ~/.lnd or ~/umbrel/lnd/ when default umbrel installation) lnd directory",
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
    check_group = parser.add_argument_group(
        "check",
        "Check if channels are open with pubkey list",
    )
    
    check_group.add_argument(
        "-pubkeys-file",
        "-pk",
        default="./pubkeys.txt",
        dest="pubkeys_file",
        help="(default ./pubkeys.txt) pubkeys file"
    )
    check_group.add_argument(
        '-w',
        '--write-channels',
        action="store_true",
        dest="write_channels",
        help="(default False) Write channels.txt"
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
