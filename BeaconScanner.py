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

    def StartScanning(self):
        while self.keepScanning:
            self.scanner.start()
            self.scanner.process(0.9)
            self.scanner.stop()

    def StopScanning(self):
        return False  # TODO

    def ProcessDiscovery(self, scanEntry, isNewDev, isNewData):
        print scanEntry.addr + " " + scanEntry.rssi
        self.beaconList[scanEntry.addr] = [scanEntry.getValueText(9), scanEntry.rssi]


scanner = BeaconScanner(0)
scanner.StartScanning()
