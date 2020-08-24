from __future__ import annotations

import random


class Point2D:
    def __init__(self, x: int = 0, y: int = 0):
        # todo accept tuple constructors. miss u java.

        self.data = (int(x), int(y))

    def __str__(self):
        return f'P2D{self.data}'

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]


    def distance_to(self, p: Point2D) -> float:
        return 0.0

    def angle_to(self, p: Point2D) -> float:
        return 0.0

    #TODO implement operators. add, subtract.

    @classmethod
    def rand(cls, min_point: Point2D = None, max_point: Point2D = None) -> Point2D:
        min_point = min_point or Point2D(0, 0)
        max_point = max_point or Point2D(1, 1)

        x = int(random.random() * (max_point.x - min_point.x))
        y = int(random.random() * (max_point.y - min_point.y))

        return Point2D(x, y)

