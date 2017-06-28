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
        self.rawBeaconRssiData = {}
        self.scanner = Scanner(hciInt)
        self.keepScanning = True
        self.rounds = 0

    def StartScanning(self,discoveryCallback, scanFinishedCallback):
        self.scanner.withDelegate(discoveryCallback)
        while self.keepScanning and self.rounds < 20:
            self.rawBeaconRssiData = {}
            self.rounds += 1
            print "Beginning round " + str(self.rounds)

            self.scanner.scan(2)

            print "Ending round " + str(self.rounds) + ". Found beacons:"

            for key, value in self.rawBeaconRssiData.items():
                average = self.CalculateAverage(value)
                self.beaconList[key] = average
                print "Found beacon - Address: " + key + "; Signal Strength: " + \
                      str(average) + "dbm;"
            scanFinishedCallback(self.beaconList)

    def StopScanning(self):
        return False  # TODO

    def ProcessDiscovery(self, scanEntry, isNewDev, isNewData):
        if scanEntry.addr in self.rawBeaconRssiData:
            self.rawBeaconRssiData[scanEntry.addr].append(scanEntry.rssi)
        else:
            self.rawBeaconRssiData[scanEntry.addr] = [scanEntry.rssi]

    def CalculateAverage(self, rssiList):
        total = 0
        for item in rssiList:
            total += (item * -1)
        return total/len(rssiList)


def FinishedCallback(data):
    return False

scanner = BeaconScanner(0)
scanner.StartScanning(BeaconDiscoveryHandler(scanner.ProcessDiscovery), FinishedCallback)
