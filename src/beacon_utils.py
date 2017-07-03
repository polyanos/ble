import math


def calculate_distance(beacon):
    ratio = beacon.rssi_mean * 1.0 / beacon.tx_power
    if ratio < 1.0:
        return math.pow(ratio, 10)
    else:
        return 0.89976 * math.pow(ratio, 7.7095) + 0.111


def calculate_rssi_mean(beacon_list):
    total = 0
    for item in beacon_list:
        total += (item.rssi * - 1)
    return total/len(beacon_list) * - 1


def print_beacon_data(beacon_list):
    for v in beacon_list:
        print v.manf + " - " + v.uuid + " - " + str(v.rssi)
    print ""


def calculate_rssi_sd(beacon_list, mean, is_sample):
    temp = 0
    for beacon in beacon_list:
        temp += math.pow(beacon.rssi - mean, 2)

    if is_sample:
        return math.sqrt(temp / (len(beacon_list) - 1))
    else:
        return math.sqrt(temp / len(beacon_list))


def filter_extremes(beacon_list, meta_data):
    limit = meta_data.rssi_mean - meta_data.rssi_sd * 2
    print "Filter limit value = " + str(limit)
    i = 0
    for beacon in beacon_list:
        if beacon.rssi < limit:
            del(beacon_list, i)
        i += 1

    return beacon_list
