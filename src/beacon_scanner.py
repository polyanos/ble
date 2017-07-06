import time
from threading import Thread

from src import beacon_utils
from src.model import beacon_list as _bl, beacon_meta_data as _bmd
from src.scanner import LowLevelScanner


class BeaconScanner(Thread):
    def __init__(self, hci_number, time_span, callback):
        Thread.__init__(self)
        self.debug = True

        self.hci_number = int(hci_number)
        self.filters = []
        self.beacon_list = {}
        self.beacon_meta_list = {}
        self.time_span = time_span
        self.callback = callback
        self.is_scanning = True

        self.scanner = LowLevelScanner(self.hci_number, self.on_discovery)

    def scan_for_beacons(self):
        self.scanner.start()

        while self.is_scanning:
            scanner_time_span = self.time_span / 1000
            print scanner_time_span
            time.sleep(10000)
            self.on_time_elapsed()



    # Adds a filtering function to the scanner, the function should accept a Beacon object and return a boolean
    def add_filter(self, filter_function):
        self.filters.append(filter_function)

    def on_discovery(self, beacon):
        if self.beacon_satisfy_filter(beacon):
            # print "Added beacon {} with tx-power of {} and rssi of {}".format(beacon.uuid, beacon.tranp, beacon.rssi)
            if beacon.uuid in self.beacon_list:
                self.beacon_list[beacon.uuid].add(beacon)
            else:
                self.beacon_list[beacon.uuid] = _bl.BeaconList(int(self.time_span / 100))

    def on_time_elapsed(self):
        return_list = []

        for k, beacon_list in self.beacon_list.items():
            meta_beacon = _bmd.BeaconMetaData(beacon_list[0].uuid)
            meta_beacon.tx_power = beacon_list[0].tranp
            meta_beacon.rssi_mean = beacon_utils.calculate_rssi_mean(beacon_list)
            meta_beacon.rssi_sd = beacon_utils.calculate_rssi_sd(beacon_list, meta_beacon.rssi_mean, True)
            meta_beacon.rssi_filtered_mean = beacon_utils.calculate_rssi_mean(beacon_utils.filter_extremes(beacon_list.items, meta_beacon))
            meta_beacon.estimated_distance = beacon_utils.calculate_distance_in_centimeters(
                meta_beacon.rssi_filtered_mean, meta_beacon.tx_power)

            return_list.append(meta_beacon)

        self.callback(return_list)

    def beacon_satisfy_filter(self, beacon):
        if len(self.filters) > 0:
            for filter_function in self.filters:
                if filter_function(beacon):
                    return True

            return False
        else:
            return True

    def run(self):
        print "Starting scanner"
        self.scan_for_beacons()
        print "Stopping scanner"

    def stop_scanning(self):
        print "Stop command for scanner received"
        self.scanner.stop()
        self.scanner.join(10)
        self.is_scanning = False
