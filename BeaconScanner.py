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
            self.scanner.start()
            self.scanner.process(1)
            self.scanner.stop()
            print "Ending round " + str(self.rounds)

    def StopScanning(self):
        return False  # TODO

    def ProcessDiscovery(self, scanEntry, isNewDev, isNewData):
        print str(scanEntry.addr) + " " + str(scanEntry.rssi)
        self.beaconList[scanEntry.addr] = [scanEntry.getValueText(9), scanEntry.rssi]


scanner = BeaconScanner(0)
scanner.StartScanning(BeaconDiscoveryHandler(scanner.ProcessDiscovery))
