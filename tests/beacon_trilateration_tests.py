import unittest

import src.model.beacon_location as _bl
import src.model.beacon_meta_data as _bmd
import src.trilateration as trilateration


class TrilaterationTests(unittest.TestCase):
    def testTrilaterationTestNotEnoughBeacons(self):
        # Arrange
        beacon_location_1 = _bl.BeaconLocation("1d7837fe978548daa9fa5ffe732b6f51", 100, 100)
        beacon_location_2 = _bl.BeaconLocation("5f6962825819435aba0dc2d1fe87deaa", 700, 100)
        beacon_location_3 = _bl.BeaconLocation("6d7b5ac1a4f245218799eb7afd4a30bd", 400, 700)
        beacon_locations = {beacon_location_1.uuid: beacon_location_1,
                            beacon_location_2.uuid: beacon_location_2,
                            beacon_location_3.uuid: beacon_location_3}

        beacon_meta_1 = _bmd.BeaconMetaData("1d7837fe978548daa9fa5ffe732b6f51")
        beacon_meta_1.estimated_distance = 250
        beacon_meta_2 = _bmd.BeaconMetaData("5f6962825819435aba0dc2d1fe87deaa")
        beacon_meta_2.estimated_distance = 300
        used_beacons = [beacon_meta_1, beacon_meta_2]

        # Act
        distance = trilateration.calculate_position(beacon_locations, used_beacons)

        # Assert
        self.assertEqual(distance[0], 0)
        self.assertEqual(distance[1], 0)

    def testTrilaterationTestEnoughBeacons(self):
        # Arrange
        beacon_location_1 = _bl.BeaconLocation("1d7837fe978548daa9fa5ffe732b6f51", 1.0, 1.0)
        beacon_location_2 = _bl.BeaconLocation("5f6962825819435aba0dc2d1fe87deaa", 999.0, 1.0)
        beacon_location_3 = _bl.BeaconLocation("6d7b5ac1a4f245218799eb7afd4a30bd", 550.0, 999.0)
        beacon_locations = {beacon_location_1.uuid: beacon_location_1,
                            beacon_location_2.uuid: beacon_location_2,
                            beacon_location_3.uuid: beacon_location_3}

        beacon_meta_1 = _bmd.BeaconMetaData("1d7837fe978548daa9fa5ffe732b6f51")
        beacon_meta_1.estimated_distance = 300.0
        beacon_meta_2 = _bmd.BeaconMetaData("5f6962825819435aba0dc2d1fe87deaa")
        beacon_meta_2.estimated_distance = 700.0
        beacon_meta_3 = _bmd.BeaconMetaData("6d7b5ac1a4f245218799eb7afd4a30bd")
        beacon_meta_3.estimated_distance = 600.0
        used_beacons = [beacon_meta_1, beacon_meta_2, beacon_meta_3]

        # Act
        distance = trilateration.calculate_position(beacon_locations, used_beacons)

        # Assert
        self.assertEqual(distance[0], 300, "found value = " + str(distance[0]))
        self.assertEqual(distance[1], 351, "found value = " + str(distance[1]))
