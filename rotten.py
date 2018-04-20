#!/usr/bin/python3
import csv
import ipaddress
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('ip', nargs='+')
args = parser.parse_args()

rotten_ips = {}
networks = []


def get_ip_list_from_dump():
    with open('dump.csv', 'r', errors='ignore') as csv_file:
        has_header = csv.Sniffer().has_header(csv_file.readline())
        csv_file.seek(0)  # Rewind
        if has_header:
            next(csv_file, None)  # Skip header row
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            for ip in row[0].split('|'):
                ip = ip.strip()
                try:
                    rotten_ips[ip2long(ip)] = ip
                except ValueError:
                    networks.append(ipaddress.ip_network(ip))


def ip2long(ip_as_str):
    return int(ipaddress.ip_address(ip_as_str))


def contains_in_single_list(ip_str):
    return ip2long(ip_str) in rotten_ips


def contains_in_networks_list(ip_str):
    ip_address = ipaddress.ip_address(ip_str)
    for network in networks:
        if ip_address in network:
            return True
    return False


def check_ip(ip_str):
    if contains_in_single_list(ip_str) or contains_in_networks_list(ip_str):
        print('BAD NEWS')
    else:
        print('GOOD NEWS')


if __name__ == '__main__':
    get_ip_list_from_dump()
    print('single ip addresses size = %s' % (len(rotten_ips)))
    print('networks size = %s' % (len(networks)))
    for ip in args.ip:
        check_ip(ip)
