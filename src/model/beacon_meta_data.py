class BeaconMetaData:
    def __init__(self, uuid):
        self._uuid = uuid
        self._rssi_mean = 0
        self._rssi_sd = 0
        self._rssi_filtered_mean = 0
        self._tx_power = 0

    @property
    def uuid(self):
        return self._uuid

    @property
    def rssi_mean(self):
        return self._rssi_mean

    @property
    def rssi_sd(self):
        return self._rssi_sd

    @property
    def rssi_filtered_mean(self):
        return self._rssi_filtered_mean

    @property
    def tx_power(self):
        return self._tx_power

    @rssi_mean.setter
    def rssi_mean(self, value):
        self._rssi_mean = value

    @rssi_sd.setter
    def rssi_sd(self, value):
        self._rssi_sd = value

    @rssi_filtered_mean.setter
    def rssi_filtered_mean(self, value):
        self._rssi_filtered_mean = value

    @tx_power.setter
    def tx_power(self, value):
        self._tx_power = value
