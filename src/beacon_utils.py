import math


def calculate_distance(rssi, tx_power):
    if False:
        ratio = rssi * 1.0 / tx_power
        if ratio < 1.0:
            return math.pow(ratio, 10)
        else:
            return 0.89976 * math.pow(ratio, 7.7095) + 0.111
    else:
        return math.pow(10.0, (tx_power - rssi) / (10.0 * 2.0))


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


def filter_extremes(list, meta_data):
    limit = meta_data.rssi_mean - meta_data.rssi_sd
    index = 0

    for beacon in list:
        if beacon.rssi < limit:
            del(list[index])

        index += 1

    return list
