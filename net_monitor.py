#!/usr/bin/env python3
""" Monitor the status (offline/online) of tracked hosts
in the local network """

import sys
import ipaddress
import platform
import subprocess


def ping(host):
    """ Pings the specified host with 1 ICMP packet """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        result = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True).lower()
        if ("unreachable" in result or
            "100% packet loss" in result):
            return False
        else:
            return True
    except subprocess.CalledProcessError:
        return False


def ping_all(hosts):
    """ Pings all the specified hosts """
    print("\nChecking hosts...")
    for host, status in hosts.items():
        hosts[host] = "ONLINE" if ping(host) else "OFFLINE"


def print_status(hosts):
    """ Prints the status of all currently tracked hosts """
    print("-" * 50)
    for host, status in hosts.items():
        print(f"Host '{host}' is {status}")
    print("-" * 50, "\n")


def valid_ip(input):
    """ Checks if the input string is a valid ip """
    try:
        ipaddress.ip_address(input)
        return True
    except ValueError:
        print(f"'{input}' is not a valid IP address")
        return False


if __name__ == "__main__":
    hosts = {}
    while True:
        command = input("Type an IP address to track, press 'enter' to update all tracked hosts or type 'q' to quit: ").strip().lower()
        match command:
            case "q":
                sys.exit(0)
            case "":
                ping_all(hosts)
                print_status(hosts)
            case _:
                if valid_ip(command):
                    hosts[command] = "UNKNOWN"
                ping_all(hosts)
                print_status(hosts)