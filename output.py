import os
import sys
from yachalk import chalk

ALIAS_LENGTH = 32


class Output:
    def __init__(self, lnd):
        self.lnd = lnd

    @staticmethod
    def print_line(message, end='\n'):
        sys.stdout.write(f"{message}{end}")

    @staticmethod
    def print_without_linebreak(message):
        sys.stdout.write(message)


def format_alias(alias):
    if not sys.stdout.encoding.lower().startswith('utf'):
        alias = alias.encode('latin-1', 'ignore').decode()
    return chalk.bold(alias)


def format_error(error):
    return chalk.red(error)


def format_channel(channel, node1_alias, node2_alias, chanDisabled, show_fees):
    text = f'{channel.channel_id:<18} {format_alias(node1_alias):<40} {format_alias(node2_alias):<40}'
    if show_fees:
        text += f'base {channel.node1_policy.fee_base_msat:<5} rate {channel.node1_policy.fee_rate_milli_msat:<5} '\
                f'base {channel.node2_policy.fee_base_msat:<5} rate {channel.node2_policy.fee_rate_milli_msat:<5} '
    if chanDisabled:
        return chalk.bg_red(text)
    else:
        return text

def format_channel_error(channelID, error):
    text = f'{channelID:<18} ERROR: {error:<100}'
    return chalk.bg_red(text)
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
