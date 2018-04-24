#!/usr/bin/python3
import csv
import ipaddress
import argparse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

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
            for ip_address in row[0].split('|'):
                ip_address = ip_address.strip()
                if not ip_address:
                    continue
                try:
                    rotten_ips[ip2long(ip_address)] = ip_address
                except ValueError:
                    networks.append(ipaddress.ip_network(ip_address))


def ip2long(ip_as_str):
    return int(ipaddress.ip_address(ip_as_str))


def contains_in_single_list(ip_str):
    ip_long = ip2long(ip_str)
    if ip_long in rotten_ips:
        return rotten_ips[ip_long]
    return None


def contains_in_networks_list(ip_str):
    ip_address = ipaddress.ip_address(ip_str)
    for network in networks:
        if ip_address in network:
            return network
    return None


def check_ip(ip_str):
    result = contains_in_single_list(ip_str) or contains_in_networks_list(ip_str)
    if result:
        logger.info('%s - BAD (%s)', ip_str, result)
    else:
        logger.info('%s - GOOD', ip_str)


if __name__ == '__main__':
    get_ip_list_from_dump()
    logger.debug('single ip addresses size = %s', len(rotten_ips))
    logger.debug('networks size = %s', len(networks))
    for ip in args.ip:
        check_ip(ip)
