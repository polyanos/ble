import sys
import math
from src.BeaconScannerV2 import BeaconScanner


def calculate_distance(beacon):
    ratio = beacon.rssi * 1.0 / beacon.tranp
    if ratio < 1.0:
        return math.pow(ratio, 10)
    else:
        return (0.89976) * math.pow(ratio,7.7095) + 0.111

scan_time_span = 1000
hci_port_number = 0

print len(sys.argv)

if len(sys.argv) == 2:
    first_par = sys.argv[1]
    if not(first_par is None):
        scan_time_span = int(first_par)

if len(sys.argv) == 3:
    second_par = sys.argv[2]
    if not(second_par is None):
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
        print "Estimated distance = " + str(calculate_distance(item))

    print ""