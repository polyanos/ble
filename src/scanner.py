import struct
import sys
import time
import bluetooth._bluetooth as bluez

from src.model import beacon_model as _bm, beacon_list as _bl
from threading import Thread


# BLE iBeaconScanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# JCS 06/07/14
class LowLevelScanner(Thread):
    DEBUG = False
    # BLE scanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
    # BLE scanner, based on https://code.google.com/p/pybluez/source/browse/trunk/examples/advanced/inquiry-with-rssi.py

    # https://github.com/pauloborges/bluez/blob/master/tools/hcitool.c for lescan
    # https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.6/lib/hci.h for opcodes
    # https://github.com/pauloborges/bluez/blob/master/lib/hci.c#L2782 for functions used by lescan

    # performs a simple device inquiry, and returns a list of ble advertizements
    # discovered device

    # NOTE: Python's struct.pack() will add padding bytes unless you make the endianness explicit. Little endian
    # should be used for BLE. Always start a struct.pack() format string with "<"
    def __init__(self, hci_socket_number, callback):
        Thread.__init__(self)

        self.LE_META_EVENT = 0x3e
        self.LE_PUBLIC_ADDRESS=0x00
        self.LE_RANDOM_ADDRESS=0x01
        self.LE_SET_SCAN_PARAMETERS_CP_SIZE=7
        self.OGF_LE_CTL=0x08
        self.OCF_LE_SET_SCAN_PARAMETERS=0x000B
        self.OCF_LE_SET_SCAN_ENABLE=0x000C
        self.OCF_LE_CREATE_CONN=0x000D

        self.LE_ROLE_MASTER = 0x00
        self.LE_ROLE_SLAVE = 0x01

        # these are actually subevents of LE_META_EVENT
        self.EVT_LE_CONN_COMPLETE=0x01
        self.EVT_LE_ADVERTISING_REPORT=0x02
        self.EVT_LE_CONN_UPDATE_COMPLETE=0x03
        self.EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE=0x04

        # Advertisment event types
        self.ADV_IND=0x00
        self.ADV_DIRECT_IND=0x01
        self.ADV_SCAN_IND=0x02
        self.ADV_NONCONN_IND=0x03
        self.ADV_SCAN_RSP=0x04

        self.is_scanning = True
        self.hci_socket_number = hci_socket_number
        self.callback = callback

    def returnnumberpacket(self, pkt):
        myInteger = 0
        multiple = 256
        for c in pkt:
            myInteger +=  struct.unpack("B",c)[0] * multiple
            multiple = 1
        return myInteger

    def returnstringpacket(self, pkt):
        myString = ""
        for c in pkt:
            myString += "%02x" % struct.unpack("B",c)[0]
        return myString

    def printpacket(self, pkt):
        for c in pkt:
            sys.stdout.write("%02x " % struct.unpack("B",c)[0])

    def get_packed_bdaddr(self, bdaddr_string):
        packable_addr = []
        addr = bdaddr_string.split(':')
        addr.reverse()
        for b in addr:
            packable_addr.append(int(b, 16))
        return struct.pack("<BBBBBB", *packable_addr)

    def packed_bdaddr_to_string(self, bdaddr_packed):
        return ':'.join('%02x' % i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

    def hci_open_dev(self, number):
        return bluez.hci_open_dev(number)

    def hci_enable_le_scan(self, sock):
        self.hci_toggle_le_scan(sock, 0x01)

    def hci_disable_le_scan(self, sock):
        self.hci_toggle_le_scan(sock, 0x00)

    def hci_toggle_le_scan(self, sock, enable):
        cmd_pkt = struct.pack("<BB", enable, 0x00)
        bluez.hci_send_cmd(sock, self.OGF_LE_CTL, self.OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

    def start_scan(self):
        sock = self.hci_open_dev(self.hci_socket_number)
        old_filter = sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)

        # perform a device inquiry on bluetooth device #0
        # The inquiry should last 8 * 1.28 = 10.24 seconds
        # before the inquiry is performed, bluez should flush its cache of
        # previously discovered devices
        flt = bluez.hci_filter_new()
        bluez.hci_filter_all_events(flt)
        bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
        sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)

        self.hci_enable_le_scan(sock)

        while self.is_scanning:
            pkt = sock.recv(255)
            ptype, event, plen = struct.unpack("BBB", pkt[:3])
            # print "--------------"
            if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
                i = 0
            elif event == bluez.EVT_NUM_COMP_PKTS:
                i = 0
            elif event == bluez.EVT_DISCONN_COMPLETE:
                i = 0
            elif event == self.LE_META_EVENT:
                subevent, = struct.unpack("B", pkt[3])
                pkt = pkt[4:]
                if subevent == self.EVT_LE_CONN_COMPLETE:
                    i = 0
                elif subevent == self.EVT_LE_ADVERTISING_REPORT:
                    # print "advertising report"
                    num_reports = struct.unpack("B", pkt[0])[0]
                    report_pkt_offset = 0
                    for i in range(0, num_reports):
                        beacon = _bm.Beacon()
                        # build the return string
                        beacon.uuid = self.returnstringpacket(pkt[report_pkt_offset - 22: report_pkt_offset - 6])
                        beacon.major = self.returnnumberpacket(pkt[report_pkt_offset - 6: report_pkt_offset - 4])
                        beacon.minor = self.returnnumberpacket(pkt[report_pkt_offset - 4: report_pkt_offset - 2])
                        beacon.tranp = struct.unpack("b", pkt[report_pkt_offset - 2])[0]
                        beacon.rssi = struct.unpack("b", pkt[report_pkt_offset - 1])[0]
                        beacon.manf = self.returnstringpacket(pkt[-26 : -22])

                        print str(beacon)
                        self.callback(beacon)

        # Restore previous filter
        sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, old_filter)
        self.hci_disable_le_scan(sock)

    def run(self):
        print "Starting low level scanner"
        self.start_scan()
        print "Stopping low level scanner"

    def stop(self):
        self.is_scanning = False
