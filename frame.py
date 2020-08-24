import logging
from typing import Optional

import numpy
import tcod

from geometry import Point2D

logger = logging.getLogger("sneak")


class Frame(tcod.Console):
    def __init__(self, width: int, height: int, order: str = 'F', buffer: Optional[numpy.ndarray] = None,
                 root_point: Point2D = Point2D(0,0)):
        super(Frame, self).__init__(height, width, order, buffer)

        # store a list of all sub-frames.
        self.children = []

        # frames have a root location. this is always relative to their
        # parent frame.
        self.root_point = root_point

    def render(self, parent):

        # call all your children to render, then blit the resulting console onto your parent
        for child in self.children:
            child.render(self)

        self.blit(parent, self.root_point.x, self.root_point.y)
