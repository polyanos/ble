import scanner
import time
import beacon_utils


class BeaconCalibrator():
    def __init__(self, uuid, hci_port_number, time_span):
        self.time_span = time_span
        self.uuid = uuid
        self.hci_port_number = hci_port_number
        self.beacon_list = []

    def calibrate_beacon(self):
        beacon_scanner = scanner.LowLevelScanner(self.hci_port_number, self.on_discovery)
        beacon_scanner.start()
        time.sleep(self.time_span / 1000.0)
        beacon_scanner.stop()
        beacon_scanner.join(5)

        if len(self.beacon_list) > 0:
            return beacon_utils.calculate_rssi_mean(self.beacon_list)
        else:
            return 0

    def on_discovery(self, beacon):
        if beacon.uuid == self.uuid:
            self.beacon_list.append(beacon)