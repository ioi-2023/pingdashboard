#!/usr/bin/env python3

import csv
import json
import time
import subprocess

from collections import defaultdict


SEATING_LAYOUT = "seating.csv"
CONTESTANT_DATA = "users.csv"
JSON_CONTESTANT_SITE = "public/site.json"
JSON_STATUS = "public/status.json"
INTERVAL_IN_SECOND = 10

def arrange_contestant_data(contestants_filename, seating_filename):
    """Read contestant data, returns a seat -> username,ip matching"""

    with open(contestants_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader, None)
        contestant_data = list(csv_reader)
    
    contestant_lookup = {}
    for contestant_row in contestant_data:
        contestant_lookup[contestant_row[4]] = contestant_row
    
    with open(seating_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        seating_data = list(csv_reader)
    
    site_map = {}
    for i in range(len(seating_data)):
        for j in range(len(seating_data[i])):
            seatcode = chr(ord('A') + i) + str(j + 1)
            user_id = seating_data[i][j]
            if user_id:
                site_map[seatcode] = { 'user': user_id, 'ip': contestant_lookup[user_id][6] }
    
    return site_map


def read_contestant_data(filename):
    """Read contestant data, returns a map of hostname to its ip address"""

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader, None)

        # change the index if csv format is changed
        return {row[6]: row[4] for row in csv_reader}


def read_status(filename):
    """Read latest status, returns a map of hostname to its latest status"""

    try:
        with open(filename) as json_file:
            status = json.load(json_file)
            return {row[0]: row[1] for row in status["results"]}

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return defaultdict(lambda: None)


def get_hosts_status(ip_to_hostname, hostname_to_status):
    """Ping all hosts, returns an array of [hostname, status] sorted by hostname"""

    cmd = ["fping", "-C", "1", "-t", "1000", "-q"] + list(ip_to_hostname.keys())
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    ip_to_status = defaultdict(lambda: None)
    for line in proc.communicate()[1].decode("utf-8").split("\n"):
        if not line:
            continue

        ip, status = line.split(" : ")
        ip = ip.strip()
        hostname = ip_to_hostname[ip]

        if status != "-" or hostname_to_status[hostname]:
            ip_to_status[ip] = status

    result = [[hostname, ip_to_status[ip]] for ip, hostname in ip_to_hostname.items()]
    return sorted(result)


if __name__ == "__main__":
    with open(JSON_CONTESTANT_SITE, "w") as json_file:
        json.dump(arrange_contestant_data(CONTESTANT_DATA, SEATING_LAYOUT), json_file)

    ip_to_hostname = read_contestant_data(CONTESTANT_DATA)

    while True:
        hostname_to_status = read_status(JSON_STATUS)

        results = get_hosts_status(ip_to_hostname, hostname_to_status)
        status = {
            "time": time.time(),
            "results": results,
        }

        with open(JSON_STATUS, "w") as json_file:
            json.dump(status, json_file)

        time.sleep(INTERVAL_IN_SECOND)
