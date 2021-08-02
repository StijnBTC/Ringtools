import os


def is_umbrel():
    return os.uname().nodename == "umbrel"
