from __future__ import annotations

class Point2D:
    def __init__(self, x: int = 0, y: int = 0):
        self.data = (x, y)

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

    #TODO impement operators. add, subtract.

