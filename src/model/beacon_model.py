class Beacon:
    def __init__(self):
        self._uuid = ""
        self._manf = ""
        self._tranp = ""
        self._rssi = ""
        self._major = ""
        self._minor = ""

    def __str__(self):
        return ("uuid: " + str(self._uuid) +
                "; manf: " + str(self._manf) +
                "; tranp: " + str(self._tranp) +
                "; rssi: " + str(self._rssi) +
                "; major: " + str(self._major) +
                "; minor: " + str(self._minor))

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        self._uuid = uuid

    @property
    def manf(self):
        return self._manf

    @manf.setter
    def manf(self, manf):
        self._manf = manf

    @property
    def tranp(self):
        return self._tranp

    @tranp.setter
    def tranp(self, tranp):
        self._tranp = tranp

    @property
    def rssi(self):
        return self._rssi

    @rssi.setter
    def rssi(self, rssi):
        self._rssi = rssi

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, major):
        self._major = major

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, minor):
        self._minor = minor
