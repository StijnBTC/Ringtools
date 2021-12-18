import os
import grpc
from time import sleep

from output import format_channel_error, format_error, clear_screen, format_channel
from yachalk import chalk


class CheckRing:
    def __init__(self, client, output, pubkeys_file, write_channels, show_fees, channels_file):
        self.client = client
        self.output = output
        self.pubkeys_file = pubkeys_file
        self.show_fees = show_fees
        self.write_channels = write_channels
        self.channels_file = channels_file

    def read_file(self, file):
        if not os.path.isfile(file):
            self.handle_error("File does not exist")
        else:
            with open(self.pubkeys_file) as file:
                return file.read().splitlines()

    def run(self):
        self.once()


    def once(self):
        pubkeys = self.read_file(self.pubkeys_file)
        channelList = []

        for idx, pubkeyInfo in enumerate(pubkeys):
            # pubkeys format is <pubkey>,<telegram username> to be able to mimic the manual pubkey overview with usernames
            pubkey = pubkeyInfo.split(',')
            try:
                alias = self.client.get_node_alias(pubkey[0])
                response = self.client.get_node_channels(pubkey[0])

                print("%s" %
                      (chalk.yellow(alias)))

                channelTo = pubkeys[(idx+1) % (len(pubkeys))].split(',')[0]
                hasChannel = False
                channelId = 0
                channelInfo = {}

                for channel in response.channels:
                    if (channel.node1_pub == channelTo) or (channel.node2_pub == channelTo):
                        hasChannel = True
                        channelId = channel.channel_id
                        channelInfo = channel
                        channelList.append(channelId)

                if hasChannel:
                    outputHas = chalk.green('✅')
                else:
                    outputHas = chalk.red('🙌🏻')
                print("%s %s\r\n%s" %
                      (outputHas, pubkey[1], pubkey[0]))

                if hasChannel:
                    print(chalk.green("Channel is open with ID: %s") % channelId)

                    if self.show_fees:
                        response = self.client.get_edge(int(channelId))
                        node1 = self.client.get_node(response.node1_pub)
                        node2 = self.client.get_node(response.node2_pub)
                        disabled = response.node1_policy.disabled or response.node2_policy.disabled
                        self.print_channel(
                            channelInfo, node1.alias, node2.alias, disabled)
                else:
                    print(chalk.red("Should open to node with pubkey %s") % channelTo)
            except grpc.RpcError as e:
                self.output.print_line(format_channel_error(pubkey, repr(e)))
            except Exception as error:
                self.output.print_line(
                    format_channel_error(pubkey, repr(error)))
        if self.write_channels:
            f = open(self.channels_file, "w")
            for c in channelList:
                f.write(str(c) + "\r\n")
            f.close()

    def print_channel(self, channel, node1_alias, node2_alias, chan_disabled):
        self.output.print_line(format_channel(
            channel, node1_alias, node2_alias, chan_disabled, self.show_fees))

    def handle_error(self, error):
        self.output.print_line(format_error(error))
