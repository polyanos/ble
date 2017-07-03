import sys
import src.beacon_utils as bu
from src.beacon_scanner import BeaconScanner

scan_time_span = 2000
hci_port_number = 0
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
    result = scanner.scan_for_time_span(scan_time_span)
    print "Ending round " + str(round_number)

    for item in result:
        print "Data of {}".format(item.uuid)
        print "Average rssi of {} dbm".format(item.rssi_mean)
        print "Filtered average rssi of {} dbm".format(item.rssi_filtered_mean)
        print "Estimated distance = " + str(bu.calculate_distance(item))

    print ""
