import math


def calculate_distance(beacon):
    ratio = beacon.rssi * 1.0 / beacon.tranp
    if ratio < 1.0:
        return math.pow(ratio, 10)
    else:
        return 0.89976 * math.pow(ratio, 7.7095) + 0.111


def calculate_average_rssi(beacon_list):
    total = 0
    for item in beacon_list.items:
        total += (item.rssi * - 1)
    return total/len(beacon_list) * - 1


def print_beacon_data(beacon_list):
    for v in beacon_list.items():
        print v.manf + " - " + v.uuid + " - " + str(v.rssi)
    print ""
