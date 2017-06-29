import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.BeaconScannerV2 import BeaconScanner

first_par = sys.argv[1]
second_par = sys.argv[2]

if first_par is None:
    scan_time_span = 1000
else:
    scan_time_span = int(first_par)

if second_par is None:
    hci_port_number = 0
else:
    hci_port_number = int(second_par)

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
        print "Estimated distance = " + str(10 ^ ((item.tranp - item.rssi)/20))

    print ""