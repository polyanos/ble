import sys
import src.beacon_utils as bu
import src.trilateration as _tr
import src.model.beacon_location as _bl
from src.beacon_scanner import BeaconScanner


def beacon_filter(beacon):
    if beacon.manf == "cdab0215":
        return True
    else:
        return False


def test_beacon_locations():
    # Should come from database
    beacon1 = _bl.BeaconLocation("1d7837fe978548daa9fa5ffe732b6f51", 1.0, 1.0)
    beacon2 = _bl.BeaconLocation("5f6962825819435aba0dc2d1fe87deaa", 6.0, 1.0)
    beacon3 = _bl.BeaconLocation("6d7b5ac1a4f245218799eb7afd4a30bd", 3.0, 6.0)
    beacon_locations = {
        beacon1.uuid: beacon1,
        beacon2.uuid: beacon2,
        beacon3.uuid: beacon3
    }
    return beacon_locations


class Main:
    def __init__(self, time_span, hci_port_number):
        self.round_number = 0
        self.time_span = time_span
        self.hci_port_number = hci_port_number

    def start_program(self):
        print "Starting program"
        scanner = BeaconScanner(self.hci_port_number, self.time_span, self.on_result)
        scanner.add_filter(beacon_filter)
        scanner.start()
        try:
            self.wait_for_input()
        except KeyboardInterrupt:
            print "User interrupted the program, exiting..."
        finally:
            scanner.stop_scanning()
            scanner.join(10)

    def on_result(self, beacon_list):
        self.round_number += 1
        print "Results of round " + str(self.round_number)
        for item in beacon_list:
            print "Data of {}".format(item.uuid)
            print "Average rssi of {} dbm".format(item.rssi_mean)
            print "Filtered average rssi of {} dbm".format(item.rssi_filtered_mean)
            print "Estimated distance = " + str(item.estimated_distance)
            print ""

        location = _tr.calculate_position(test_beacon_locations(), beacon_list)
        print "Estimated location is: x = {}m; y = {}m".format(location[0], location[1])

    def wait_for_input(self):
        raw_input("Press a key to exit...")
        return False

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

main = Main(scan_time_span, hci_port_number)
main.start_program()
