import math


class base_station(object):
    def __init__(self, lat, lon, dist):
        self.lat = lat
        self.lon = lon
        self.dist = dist


class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class circle(object):
    def __init__(self, point, radius):
        self.center = point
        self.radius = radius


class json_data(object):
    def __init__(self, circles, inner_points, center):
        self.circles = circles
        self.inner_points = inner_points
        self.center = center


def serialize_instance(obj):
    d = {}
    d.update(vars(obj))
    return d


def get_two_points_distance(p1, p2):
    return math.sqrt(pow((p1.x - p2.x), 2) + pow((p1.y - p2.y), 2))


def get_two_circles_intersecting_points(c1, c2):
    p1 = c1.center
    p2 = c2.center
    r1 = c1.radius
    r2 = c2.radius

    d = get_two_points_distance(p1, p2)
    # if to far away, or self contained - can't be done
    if d >= (r1 + r2) or d <= math.fabs(r1 - r2):
        return None

    a = (pow(r1, 2) - pow(r2, 2) + pow(d, 2)) / (2 * d)
    h = math.sqrt(pow(r1, 2) - pow(a, 2))
    x0 = p1.x + a * (p2.x - p1.x) / d
    y0 = p1.y + a * (p2.y - p1.y) / d
    rx = -(p2.y - p1.y) * (h / d)
    ry = -(p2.x - p1.x) * (h / d)
    return [point(x0 + rx, y0 - ry), point(x0 - rx, y0 + ry)]


def get_all_intersecting_points(circles):
    points = []
    num = len(circles)
    for i in range(num):
        j = i + 1
        for k in range(j, num):
            res = get_two_circles_intersecting_points(circles[i], circles[k])
            if res:
                points.extend(res)
    return points


def is_contained_in_circles(point, circles):
    for i in range(len(circles)):
        if (get_two_points_distance(point, circles[i].center) > (circles[i].radius)):
            return False
    return True


def get_polygon_center(points):
    center = point(0, 0)
    num = len(points)
    for i in range(num):
        center.x += points[i].x
        center.y += points[i].y
    center.x /= num
    center.y /= num
    return center


def calculate_position(beacon_locations, used_beacons):
    # Need at least 3 beacons to get a position
    if len(used_beacons) < 3:
        return [0, 0]

    # Sort the list to use the closest 3 points
    sorted_beacons = sorted(used_beacons, key=lambda x: x.rssi_filtered_mean, reverse=False)

    # starting x,y, and z(radius is the RSSI of beacon) locations of circles
    c1 = circle(point(beacon_locations[sorted_beacons[0].uuid].west_distance,
                      beacon_locations[sorted_beacons[0].uuid].north_distance),
                sorted_beacons[0].estimated_distance)
    c2 = circle(point(beacon_locations[sorted_beacons[1].uuid].west_distance,
                      beacon_locations[sorted_beacons[1].uuid].north_distance),
                sorted_beacons[1].estimated_distance)
    c3 = circle(point(beacon_locations[sorted_beacons[2].uuid].west_distance,
                      beacon_locations[sorted_beacons[2].uuid].north_distance),
                sorted_beacons[2].estimated_distance)

    p1 = point(0.81, 1.2)
    p2 = point(1.21, 0.69)
    p3 = point(0.87, 0.84)

    c1 = circle(p1, 0.70)
    c2 = circle(p2, 0.51)
    c3 = circle(p3, 0.63)

    circle_list = [c1, c2, c3]

    inner_points = []
    for p in get_all_intersecting_points(circle_list):
        if is_contained_in_circles(p, circle_list):
            inner_points.append(p)

    center = get_polygon_center(inner_points)
    print center.x, center.y
    return [center.x, center.y]
