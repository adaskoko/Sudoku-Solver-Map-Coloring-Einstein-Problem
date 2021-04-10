import random
import sys
import math
from shapely.geometry import LineString
import matplotlib.pyplot as plt


COLORS = {1: "red",
          2: "green",
          3: "blue",
          4: "black"}


def two_lines_crossing(line1, line2):
    line_1 = LineString([(line1.point1.x, line1.point1.y), (line1.point2.x, line1.point2.y)])
    line_2 = LineString([(line2.point1.x, line2.point1.y), (line2.point2.x, line2.point2.y)])
    return line_1.intersects(line_2) and line1.point1 is not line2.point1 and line1.point1 is not line2.point2 \
        and line1.point2 is not line2.point1 and line1.point2 is not line2.point2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connected_points = []
        self.color = None


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2


class Map:
    def __init__(self):
        self.points = []
        self.lines = []
        self.number_of_pts = 0

    def generate_points(self, number_of_pts):
        self.number_of_pts = number_of_pts
        for i in range(number_of_pts):
            x = random.random()
            y = random.random()
            self.points.append(Point(x, y))

    def connect_points(self):
        points_not_able_to_connect = []

        while len(points_not_able_to_connect) < self.number_of_pts:
            point1 = self.points[random.randint(0, self.number_of_pts - 1)]
            while point1 in points_not_able_to_connect:
                point1 = self.points[random.randint(0, self.number_of_pts - 1)]

            point2 = self._get_closest_point(point1)
            line = Line(point1, point2)

            if point2 is not None:
                self.lines.append(line)
                point1.connected_points.append(point2)
                point2.connected_points.append(point1)
            else:
                points_not_able_to_connect.append(point1)

    def draw(self):
        for i in range(0, len(self.lines)):
            plt.plot([self.lines[i].point1.x, self.lines[i].point2.x],
                     [self.lines[i].point1.y, self.lines[i].point2.y], color="gray")

        for point in self.points:
            if point.color is not None:
                plt.plot(point.x, point.y, "o", color=COLORS[point.color])

        plt.show()

    def _get_closest_point(self, point):
        distance = sys.float_info.max
        closest_point = None

        for point2 in self.points:
            if point2 is not point and point2 not in point.connected_points:
                dist = math.sqrt((point.x - point2.x) ** 2 + (point.y - point2.y) ** 2)
                if dist < distance and self._not_crossing(Line(point, point2)):
                    distance = dist
                    closest_point = point2

        return closest_point

    def _not_crossing(self, line):
        for checked_line in self.lines:
            if two_lines_crossing(line, checked_line):
                return False
        return True

