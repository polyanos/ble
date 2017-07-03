from src import scanner, beacon_utils
from src.model import beacon_list as _bl, beacon_meta_data as _bmd


class BeaconScanner:
    def __init__(self, hci_number):
        self.debug = True

        self.hci_number = hci_number
        self.filters = []
        self.beacon_list = {}
        self.beacon_meta_list = {}

    def scan_for_time_span(self, time_span):
        sock = scanner.hci_open_dev(self.hci_number)
        result = scanner.start_scan(sock, time_span, self.on_discovery)
        return_list = []

        for k, beacon_list in result.items():
            if self.debug:
                beacon_utils.print_beacon_data(beacon_list)

            meta_beacon = _bmd.BeaconMetaData(beacon_list[0].uuid)
            meta_beacon.mean = beacon_utils.calculate_rssi_mean(beacon_list)
            meta_beacon.sd = beacon_utils.calculate_rssi_sd(beacon_list, meta_beacon.mean, True)
            meta_beacon.tx_power = beacon_list[0].tranp
            filtered_beacons = beacon_utils.filter_extremes(beacon_list, meta_beacon)
            meta_beacon.rssi_filtered_mean = beacon_utils.calculate_rssi_mean(filtered_beacons)

            return_list.append(meta_beacon)

        return return_list

    # Adds a filtering function to the scanner, the function should accept a Beacon object and return a boolean
    def add_filter(self, filter_function):
        self.filters.append(filter_function)

    def on_discovery(self, beacon):
        if self.beacon_satisfy_filter(beacon):
            if beacon.uuid in self.beacon_list:
                self.beacon_list[beacon.uuid].add(beacon)
            else:
                self.beacon_list[beacon.uuid] = _bl.BeaconList(10)

    def beacon_satisfy_filter(self, beacon):
        if len(self.filters) > 1:
            for filter_function in self.filters:
                if filter_function(beacon):
                    return True

            return False
        else:
            return True
