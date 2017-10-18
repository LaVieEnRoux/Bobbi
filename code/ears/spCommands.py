from __future__ import print_function

import subprocess

# make sure that sp (Spotify bash interface) is in the system $PATH

commands = ["play", "pause", "next", "prev", "art", "open"]

# specify what is required for each command type
no_arg_commands = ["play", "pause", "next", "prev"]
return_commands = ["art"]
arg_commands = ["open"]


def send_command(commandType, arg=""):
    ''' send command to sp '''

    if commandType not in commands:
        print("Incorrect type of command: {}".format(commandType))
        raise ValueError("Bad SP command")

    if commandType in no_arg_commands:
        ret = subprocess.call(["sp", commandType])

    if commandType in return_commands:
        ret = subprocess.check_output(["sp", commandType])

    if commandType in arg_commands:
        ret = subprocess.call(["sp", commandType, arg])

    return ret
