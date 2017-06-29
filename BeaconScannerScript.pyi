from BeaconScannerV2 import BeaconScanner

hci_port_number = 0
scan_time_span = 1000
scanner = BeaconScanner(hci_port_number)
round_number = 0

while True:
    round_number += 1
    print("Starting round " + round_number)
    scanner.scan_for_timespan(scan_time_span)
    print("Ending round "  + round_number)
    print("")