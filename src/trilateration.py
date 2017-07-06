# From https://stackoverflow.com/questions/30336278/multi-point-trilateration-algorithm-in-java

import src.model.beacon_circle as _c
# room specs: width = 1.5m, height = 2m
# beacon positions: 1m,1m;6m,1m;3m,6m


def _get_location(circle1, circle2, circle3):
    # calculate the center
    a1 = (-circle1.x * 2)
    b1 = (circle1.x ** 2)
    c1 = (-circle1.y * 2)
    d1 = (circle1.y ** 2)
    e1 = (circle1.distance ** 2)
    # print a1, b1, c1, d1, e1

    a2 = (-circle2.x * 2)
    b2 = (circle2.x ** 2)
    c2 = (-circle2.y * 2)
    d2 = (circle2.y ** 2)
    e2 = (circle2.distance ** 2)
    # print a2, b2, c2, d2, e2

    a3 = (-circle3.x * 2)
    b3 = (circle3.x ** 2)
    c3 = (-circle3.y * 2)
    d3 = (circle3.y ** 2)
    e3 = (circle3.distance ** 2)
    # print a3, b3, c3, d3, e3

    # print a1 - a2, b1 - b2, c1 - c2, d1 - d2, e1 - e2
    a = a1 - a2
    b = b1 - b2
    c = c1 - c2
    d = d1 - d2
    e = e1 - e2
    e -= b
    e -= d
    a = -a
    if not c == 0:
        e = e / float(c)
        a = a / float(c)

    # print "y1", a, e

    a2 = a2 - a3
    b2 = b2 - b3
    c2 = c2 - c3
    d2 = d2 - d3
    e2 = e2 - e3
    e2 -= b2
    e2 -= d2
    a2 = -a2
    e2 = e2 / float(c2)
    a2 = a2 / float(c2)
    # print "y2", a2, e2

    a5 = e2 - e
    b5 = abs(a2) + a
    x = a5 / b5
    # print b5, a5
    # print "x=", x

    y = round((a2 * x) + e2, 0)
    x = round(x, 0)
    # print "y=", y
    print "Cart location is approximately: x = {}cm; y = {}cm".format(x, y)
    return [x, y]


# used_beacons = list of BeaconMetaData objects
# beacon_locations = dictionary of BeaconLocation objects, with uuid as keys
def calculate_position(beacon_locations, used_beacons):
    # Need at least 3 beacons to get a position
    if len(used_beacons) < 3:
        return [0, 0]

    # Sort the list to use the closest 3 points
    sorted_beacons = sorted(used_beacons, key=lambda x: x.rssi_filtered_mean, reverse=False)
    for i in sorted_beacons:
        print beacon_locations[i.uuid].west_distance, beacon_locations[i.uuid].north_distance, i.estimated_distance


    # starting x,y, and z(radius is the RSSI of beacon) locations of circles
    circle1 = _c.BeaconCirlce(beacon_locations[sorted_beacons[0].uuid].west_distance,
                              beacon_locations[sorted_beacons[0].uuid].north_distance,
                              sorted_beacons[0].estimated_distance)
    circle2 = _c.BeaconCirlce(beacon_locations[sorted_beacons[1].uuid].west_distance,
                              beacon_locations[sorted_beacons[1].uuid].north_distance,
                              sorted_beacons[1].estimated_distance)
    circle3 = _c.BeaconCirlce(beacon_locations[sorted_beacons[2].uuid].west_distance,
                              beacon_locations[sorted_beacons[2].uuid].north_distance,
                              sorted_beacons[2].estimated_distance)

    return _get_location(circle1, circle2, circle3)
