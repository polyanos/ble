# From https://github.com/dvalenza/Trilateration-Example/blob/master/trilaterate.py

import src.model.beacon_location as _bl

# room specs: width = 6m, height = 6m
# beacon positions: 1m,1m;6m,1m;3m,6m

def getlocation(xA, yA, zA, xB, yB, zB, xC, yC, zC):
    # calculate the center
    A1 = (-(xA) * 2)
    B1 = ((xA) ** 2)
    C1 = (-(yA) * 2)
    D1 = ((yA) ** 2)
    E1 = ((zA) ** 2)
    # print A1, B1, C1, D1, E1

    A2 = (-(xB) * 2)
    B2 = ((xB) ** 2)
    C2 = (-(yB) * 2)
    D2 = ((yB) ** 2)
    E2 = ((zB) ** 2)
    # print A2, B2, C2, D2, E2

    A3 = (-(xC) * 2)
    B3 = ((xC) ** 2)
    C3 = (-(yC) * 2)
    D3 = ((yC) ** 2)
    E3 = ((zC) ** 2)
    # print A3, B3, C3, D3, E3

    # print A1 - A2, B1 - B2, C1 - C2, D1 - D2, E1 - E2
    A = A1 - A2
    B = B1 - B2
    C = C1 - C2
    D = D1 - D2
    E = E1 - E2
    E -= B
    E -= D
    A = -A
    if not C == 0:
        E = E / float(C)
        A = A / float(C)

    # print "y1", A, E

    A2 = A2 - A3
    B2 = B2 - B3
    C2 = C2 - C3
    D2 = D2 - D3
    E2 = E2 - E3
    E2 -= B2
    E2 -= D2
    A2 = -A2
    if not C2 == 0:
        E2 = E2 / float(C2)
        A2 = A2 / float(C2)
    # print "y2", A2, E2

    A5 = E2 - E
    B5 = abs(A2) + A
    if not B5 == 0:
        x = A5 / B5
    else:
        x = A5
    # print B5, A5
    # print "x=", x

    y = (A2 * x) + E2
    # print "y=", y
    print "Cart location is approximately: x = {}m; y = {}m".format(x, y)
    return [x, y]

# used_beacons = list of BeaconMetaData objects
# beacon_locations = dictionary of BeaconLocation objects, with uuid as keys
def calculate_position(beacon_locations, used_beacons):
    # Need at least 3 beacons to get a position
    if len(used_beacons) < 3:
        return [0,0]

    # Sort the list to use the closest 3 points
    sorted_beacons = sorted(used_beacons, key=lambda x: x.rssi_filtered_mean, reverse=False)

    # starting x,y, and z(radius is the RSSI of beacon) locations of circles
    xA = beacon_locations[sorted_beacons[0].uuid].west_distance
    yA = beacon_locations[sorted_beacons[0].uuid].north_distance
    zA = sorted_beacons[0].estimated_distance
    xB = beacon_locations[sorted_beacons[1].uuid].west_distance
    yB = beacon_locations[sorted_beacons[1].uuid].north_distance
    zB = sorted_beacons[1].estimated_distance
    xC = beacon_locations[sorted_beacons[2].uuid].west_distance
    yC = beacon_locations[sorted_beacons[2].uuid].north_distance
    zC = sorted_beacons[2].estimated_distance

    print "Beacon 1: x = {}m; y = {}m;\nDistance from beacon is approximately {}m\n"\
        .format(xA, yA, zA)
    print "Beacon 2: x = {}m; y = {}m;\nDistance from beacon is approximately {}m\n"\
        .format(xB, yB, zB)
    print "Beacon 3: x = {}m; y = {}m;\nDistance from beacon is approximately {}m\n"\
        .format(xC, yC, zC)

    return getlocation(xA, yA, zA, xB, yB, zB, xC, yC, zC)