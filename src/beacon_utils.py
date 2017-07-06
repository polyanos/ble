import math


def calculate_distance_in_centimeters(rssi, tx_power):
    ratio = rssi * 1.0 / tx_power

    return 10 ^ ((tx_power - rssi) / 20)
    if ratio < 1.0:
        return round(math.pow(ratio, 10) * 100, 0)
    else:
        return round((0.89976 * math.pow(ratio, 7.7095) + 0.111) * 100, 0)

def calculate_rssi_mean(beacon_list):
    total = 0
    for item in beacon_list:
        total += item.rssi
    return total/len(beacon_list)


def print_beacon_data(beacon_list):
    for v in beacon_list:
        print v.manf + " - " + v.uuid + " - " + str(v.rssi)
    print ""


def calculate_rssi_sd(beacon_list, mean, is_sample):
    if len(beacon_list) < 2:
        return 0

    temp = 0
    for beacon in beacon_list:
        temp += math.pow(beacon.rssi - mean, 2)

    if is_sample:
        return math.sqrt(temp / (len(beacon_list) - 1))
    else:
        return math.sqrt(temp / len(beacon_list))


def filter_extremes(list, meta_data):
    under_limit = meta_data.rssi_mean + meta_data.rssi_sd * 1.5
    upper_limit = meta_data.rssi_mean - meta_data.rssi_sd * 1.5
    index = 0

    for beacon in list:
        if beacon.rssi < upper_limit or beacon.rssi > under_limit:
            del(list[index])

        index += 1

    return list
