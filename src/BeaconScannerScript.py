import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.BeaconScannerV2 import BeaconScanner

hci_port_number = 0
scan_time_span = 1000
scanner = BeaconScanner(hci_port_number)
round_number = 0
result = []

while True:
    round_number += 1
    print "Starting round " + str(round_number)
    result = scanner.scan_for_timespan(scan_time_span)
    print "Ending round "  + str(round_number)

    for item in result:
        print "Average rssi of " + item.uuid + " = " + str(item.rssi) + "dbm"
        print "Estimated distance = " + str(10 ^ ((item.tranp - item.RSSI)/20))

    print ""