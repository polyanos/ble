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
            self.scanner.scan(2)

            for key, value in self.rawBeaconRssiData.items():
                self.beaconList[key] = self.CalculateAverage(value)

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
        return total/len(rssiList) * -1


def FinishedCallback(data):
    for key, value in data.items():
        print key + " " + str(value)
    return False  # TODO

scanner = BeaconScanner(0)
scanner.StartScanning(BeaconDiscoveryHandler(scanner.ProcessDiscovery), FinishedCallback)
