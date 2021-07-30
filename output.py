import os
import sys
from yachalk import chalk


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


def format_channel(channel_id, node1_alias, node2_alias, chanDisabled):
    text = f'{channel_id:<18} {format_alias(node1_alias):<32} {format_alias(node2_alias):<32}'
    if chanDisabled:
        return chalk.bg_red(text)
    else:
        return text


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
