import os
import re
from time import sleep

from output import format_error, Output, format_alias, clear_screen, format_channel

LOOP_SLEEP_TIME = 10


class Status:
    def __init__(self, lnd, output, channels_file, keep_loop):
        self.lnd = lnd
        self.output = output
        self.channels_file = channels_file
        self.keep_loop = keep_loop
        print(channels_file)

    def read_file(self, file):
        if not os.path.isfile(file):
            self.handle_error("File does not exist")
        else:
            with open(self.channels_file) as file:
                return file.read().splitlines()

    def run(self):
        if self.keep_loop:
            self.loop()
        else:
            self.once()

    def loop(self):
        while True:
            clear_screen()
            self.once()
            sleep(LOOP_SLEEP_TIME)

    def once(self):
        channels = self.read_file(self.channels_file)
        for channelID in channels:
            response = self.lnd.get_edge(int(channelID))
            node1 = self.lnd.get_node(response.node1_pub)
            node2 = self.lnd.get_node(response.node2_pub)
            disabled = response.node1_policy.disabled or response.node2_policy.disabled
            self.print_channel(response.channel_id, node1.alias, node2.alias, disabled)

    def print_channel(self, channel_id, node1_alias, node2_alias, chan_disabled):
        self.output.print_line(format_channel(channel_id, node1_alias, node2_alias, chan_disabled))

    def handle_error(self, error):
        self.output.print_line(format_error(error))
