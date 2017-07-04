import unittest
import math
import src.model.beacon_model as _bm
import src.beacon_utils as beacon_utils
import src.model.beacon_meta_data as _bmd


class BeaconUtilsTest(unittest.TestCase):
    def testCalculateDistanceRssiSmallerThenTxPower(self):
        # Arrange
        beacon = _bm.Beacon()
        beacon.rssi = -35
        beacon.tranp = -59

        expected_result = math.pow(beacon.rssi * 1.0 / beacon.tranp, 10)

        # Act
        result = beacon_utils.calculate_distance(beacon.rssi, beacon.tranp)

        # Assert
        self.assertTrue(result == expected_result)  # ~0.00539709

    def testCalculateDistanceRssiBiggerThenTxPower(self):
        # Arrange
        beacon = _bm.Beacon()
        beacon.rssi = -75
        beacon.tranp = -59

        expected_result = 0.89976 * math.pow(beacon.rssi * 1.0 / beacon.tranp, 7.7095) + 0.111

        # Act
        result = beacon_utils.calculate_distance(beacon.rssi, beacon.tranp)

        # Assert
        self.assertTrue(result == expected_result)  # ~5.8327372

    def testCalculateRssiMean1Element(self):
        # Arrange
        beacon = _bm.Beacon()
        beacon.rssi = -69
        beacon_list = [beacon]

        expected_result = -69

        # Act
        result = beacon_utils.calculate_rssi_mean(beacon_list)

        # Assert
        self.assertTrue(result == expected_result)  # -69

    def testCalculateRssiMeanMultipleElements(self):
        # Arrange
        beacon1 = _bm.Beacon()
        beacon1.rssi = -69
        beacon2 = _bm.Beacon()
        beacon2.rssi = -43
        beacon3 = _bm.Beacon()
        beacon3.rssi = -65
        beacon4 = _bm.Beacon()
        beacon4.rssi = -55
        beacon5 = _bm.Beacon()
        beacon5.rssi = -57
        beacon6 = _bm.Beacon()
        beacon6.rssi = -62
        beacon_list = [beacon1, beacon2, beacon3, beacon4, beacon5, beacon6]

        expected_result = (-69 + -43 + -65 + -55 + -57 + -62) / 6

        # Act
        result = beacon_utils.calculate_rssi_mean(beacon_list)

        # Assert
        self.assertTrue(result == expected_result) # -58.5

    def testCalculateRssiSdSingleElement(self):
        # Arrange
        beacon = _bm.Beacon()
        beacon.rssi = -69
        beacon_list = [beacon]
        mean = -69
        is_sample = True

        expected_result = 0

        # Act
        result = beacon_utils.calculate_rssi_sd(beacon_list, mean, is_sample)

        # Assert
        self.assertTrue(result == expected_result)

    def testCalculateRssiSdMultipleElementsIsSample(self):
        # Arrange
        beacon1 = _bm.Beacon()
        beacon1.rssi = -69
        beacon2 = _bm.Beacon()
        beacon2.rssi = -43
        beacon3 = _bm.Beacon()
        beacon3.rssi = -65
        beacon4 = _bm.Beacon()
        beacon4.rssi = -55
        beacon5 = _bm.Beacon()
        beacon5.rssi = -57
        beacon6 = _bm.Beacon()
        beacon6.rssi = -62
        beacon_list = [beacon1, beacon2, beacon3, beacon4, beacon5, beacon6]
        mean = -58.5
        is_sample = True

        expected_result = math.sqrt((math.pow(beacon1.rssi - mean, 2) +
                                     math.pow(beacon2.rssi - mean, 2) +
                                     math.pow(beacon3.rssi - mean, 2) +
                                     math.pow(beacon4.rssi - mean, 2) +
                                     math.pow(beacon5.rssi - mean, 2) +
                                     math.pow(beacon6.rssi - mean, 2))
                                    / (len(beacon_list) - 1))

        # Act
        result = beacon_utils.calculate_rssi_sd(beacon_list, mean, is_sample)

        # Assert
        self.assertTrue(result == expected_result)

    def testCalculateRssiSdMultipleElementsIsNotSample(self):
        # Arrange
        beacon1 = _bm.Beacon()
        beacon1.rssi = -69
        beacon2 = _bm.Beacon()
        beacon2.rssi = -43
        beacon3 = _bm.Beacon()
        beacon3.rssi = -65
        beacon4 = _bm.Beacon()
        beacon4.rssi = -55
        beacon5 = _bm.Beacon()
        beacon5.rssi = -57
        beacon6 = _bm.Beacon()
        beacon6.rssi = -62
        beacon_list = [beacon1, beacon2, beacon3, beacon4, beacon5, beacon6]
        mean = -58.5
        is_sample = False

        expected_result = math.sqrt((math.pow(beacon1.rssi - mean, 2) +
                                     math.pow(beacon2.rssi - mean, 2) +
                                     math.pow(beacon3.rssi - mean, 2) +
                                     math.pow(beacon4.rssi - mean, 2) +
                                     math.pow(beacon5.rssi - mean, 2) +
                                     math.pow(beacon6.rssi - mean, 2))
                                    / (len(beacon_list)))

        # Act
        result = beacon_utils.calculate_rssi_sd(beacon_list, mean, is_sample)

        # Assert
        self.assertTrue(result == expected_result)

    def testFilterExtremes(self):
        # Arrange
        beacon1 = _bm.Beacon()
        beacon1.rssi = -54
        beacon2 = _bm.Beacon()
        beacon2.rssi = -99
        beacon3 = _bm.Beacon()
        beacon3.rssi = -60
        beacon4 = _bm.Beacon()
        beacon4.rssi = -58
        beacon5 = _bm.Beacon()
        beacon5.rssi = -52
        beacon6 = _bm.Beacon()
        beacon6.rssi = -57
        beacon_list = [beacon1, beacon2, beacon3, beacon4, beacon5, beacon6]

        beacon_meta = _bmd.BeaconMetaData("id")
        beacon_meta.rssi_mean = -63.33333
        beacon_meta.rssi_sd = 17.70499

        expected_results = [beacon1, beacon3, beacon4, beacon5, beacon6]
        # Act
        result = beacon_utils.filter_extremes(beacon_list, beacon_meta)

        # Assert
        self.assertTrue(len(result) == len(expected_results))

        for i in range(0,len(result)):
            self.assertEqual(result[i], expected_results[i])