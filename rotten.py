import csv
import socket
import struct

rotten_ips = {}
domain_names = []


def ip2long(ip_as_str):
    packed = socket.inet_aton(ip_as_str)
    ip_as_long = struct.unpack("!L", packed)[0]
    return ip_as_long


with open('dump.csv', 'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    raw_list = []
    for row in reader:
        for ip in row[0].split('|'):
            ip = ip.strip()
            try:
                rotten_ips[ip2long(ip)] = ip
            except Exception:
                print(ip)
                domain_names.append(ip)


def check_ip(ip_str_format):
    if ip2long(ip_str_format) in rotten_ips:
        print('BAD NEWS')
    else:
        print('GOOD NEWS')


print('size = %s' % (len(rotten_ips)))
# BAD NEWS
check_ip('87.117.232.174')
# BAD NEWS
# BROKEN cause range not parsed correctly
check_ip('74.82.64.1')
# GOOD NEWS
check_ip('192.168.99.11')
