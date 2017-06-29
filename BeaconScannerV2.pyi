import blescan

class BeaconScanner():
    def __init__(self, hci_number):
        self.hci_number = hci_number

    def scan_for_timespan(self, timespan):
        sock = blescan.hci_open_dev(self.hci_number)
        result = blescan.start_scan(sock, timespan, beacon_filter)
        return_list = []

        self._print_all_data(result)
        for k, v in result.items():
            temp = v[0]
            temp.rssi = self._calculate_average_rssi(v)
            return_list.append(temp)

        return return_list

    def _calculate_average_rssi(self, beacon_sub_list):
        total = 0
        for item in beacon_sub_list:
            total += (item.rssi * -1)
        return total/len(beacon_sub_list) * -1

    def _print_all_data(self, beacon_list):
        for k, v_list in beacon_list.items():
            print("//" + k + "//")
            for v in v_list:
                print(v.manf + " - " + v.uuid + " - " + str(v.rssi))
            print()


def beacon_filter(beacon):
    if beacon.manf == "cdab0215":
        return True
    else:
        return False