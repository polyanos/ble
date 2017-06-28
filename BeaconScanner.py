#!/bin/sh
from bluepy.btle import UUID, Peripheral, Scanner, ScanEntry, DefaultDelegate


class BeaconDiscoveryHandler(DefaultDelegate):
    def __init__(self, func):
        DefaultDelegate.__init__(self)
        self.func = func

    def handleDiscovery(self, scanEntry, isNewDev, isNewData):
        self.func(scanEntry, isNewDev, isNewData)

    def handleNotification(self, cHandle, data):
        return False


class BeaconScanner():
    def __init__(self, hciInt):
        self.beaconList = {}
        self.scanner = Scanner(hciInt)
        self.keepScanning = True
        self.rounds = 0


    def StartScanning(self,callback):
        self.scanner.withDelegate(callback)
        while self.keepScanning and self.rounds < 20:
            self.rounds += 1
            print "Beginning round " + str(self.rounds)
            self.scanner.scan(2)
            print "Ending round " + str(self.rounds) + ". Found beacons:"
            for key, value in self.beaconList.items():
                print "Found beacon - Address: " + key + "; Signal Strength: " + \
                      str(value) + "dbm;"

    def StopScanning(self):
        return False  # TODO

    def ProcessDiscovery(self, scanEntry, isNewDev, isNewData):
        self.beaconList[scanEntry.addr] = [scanEntry.getValueText(9), scanEntry.rssi]


scanner = BeaconScanner(0)
scanner.StartScanning(BeaconDiscoveryHandler(scanner.ProcessDiscovery))
