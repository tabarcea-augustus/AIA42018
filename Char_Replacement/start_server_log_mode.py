#!/usr/bin/env python3
import subprocess
import sys
import time

SERVER_SCRIPT_NAME = "server.py"
SERVER_LOCATION = ""


def start_server(staring_script_name):
    command = sys.executable + " " + staring_script_name

    server_stdout = open("server_stdout.out", "w")
    server_stderr = open("server_stderr.out", "w")

    proc = subprocess.Popen(command, stdout=server_stdout, stderr=server_stderr, shell=True)
    while proc.poll() is None:
        time.sleep(10)


if __name__ == '__main__':
    start_server(SERVER_SCRIPT_NAME)
