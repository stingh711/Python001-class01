import argparse
import ipaddress
import os
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from itertools import product


def ping(ip):
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        return ip
    return None


def ping_port(ip, port):
    response = os.system(f"nc -v -z {ip} {port}")
    if response == 0:
        return port
    return None


def ping_port_wrapper(t):
    (ip, port) = t
    return ping_port(ip, port)


def parse_ip_range(ip):
    [start, end] = ip.split("-")
    parts = start.split(".")[:-1]
    parts.append("0")
    network = ipaddress.ip_network(".".join(parts) + "/24")
    hosts = [
        str(i)
        for i in network.hosts()
        if i >= ipaddress.ip_address(start) and i <= ipaddress.ip_address(end)
    ]
    return hosts


def write_file(data, file_name):
    with open(file_name, "w") as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="specify test method, ping or tcp", default="ping")
    parser.add_argument("-n", type=int, help="specify concurrency number", default="4")
    parser.add_argument("-ip", help="specify ip range")
    parser.add_argument("-w", help="speicify file name")
    parser.add_argument("-m", help="specify concurrency model", default="thread")

    args = parser.parse_args()
    workers = args.n
    ip = args.ip
    model = args.m

    if model == "thread":
        Pool = ThreadPoolExecutor
    else:
        Pool = ProcessPoolExecutor

    if args.f == "tcp":
        data = product([ip], range(1, 10000))
        with Pool(workers) as pool:
            raw_results = pool.map(ping_port_wrapper, data)

        results = sorted([r for r in raw_results if r is not None])
    elif args.f == "ping":
        ip_range = parse_ip_range(ip)
        with Pool(workers) as pool:
            raw_results = pool.map(ping, ip_range)

        results = [r for r in raw_results if r is not None]

    print(results)
    if args.w:
        write_file(results, args.w)
