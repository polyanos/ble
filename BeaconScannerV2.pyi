import blescan

class BeaconScanner():
    def __init__(self, hci_number):
        self.hci_number = hci_number


    def scan_for_time(self, timespan):
        sock = blescan.hci_open_dev(self.hci_number)
        blescan.parse_events(sock, timespan)

scanner = BeaconScanner(0)
scanner.scan_for_time(500)