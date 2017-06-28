import blescan

class BeaconScanner():
    def __init__(self, hci_number):
        self.hci_number = hci_number


    def scan_for_time(self, timespan):
        sock = blescan.hci_open_dev(self.hci_number)
        result = blescan.start_scan(sock, timespan, beacon_filter)

        for k, v in result.items():
            print v[0].uuid

        return False



def beacon_filter(beacon):
    if beacon._manf == "cdab0215":
        return True
    else:
        return False

scanner = BeaconScanner(0)
scanner.scan_for_time(1000)