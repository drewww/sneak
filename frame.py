from __future__ import annotations

import logging
import time
from typing import Optional

import numpy
import tcod

import color
from geometry import Point2D

logger = logging.getLogger("sneak")


class Frame(tcod.Console):
    def __init__(self, width: int, height: int, order: str = 'F', buffer: Optional[numpy.ndarray] = None,
                 root_point: Point2D = Point2D(0, 0)):
        super().__init__(width, height, order, buffer)

        # store a list of all sub-frames.
        self.children = []

        # frames have a root location. this is always relative to their
        # parent frame.
        self.root_point = root_point

    def render(self, parent: Frame = None):
        # call all your children to render, then blit the resulting console onto your parent
        for child in self.children:
            child.render(self)

        if parent:
            self.blit(parent, self.root_point.x, self.root_point.y)
        else:
            logger.debug("Rendering root, no parent.")

    def add_child(self, frame):
        self.children.append(frame)

    def remove_child(self, frame):
        self.children.remove(frame)

    def __str__(self):
        return f'<Frame width={self.width} height={self.height} root_point={self.root_point}>'

    # todo will need z index ordering control


class TestFrame(Frame):
    # default to 1,1 in size
    def __init__(self, width=1, height=1, order='F', buffer=None, root_point=Point2D(0, 0)):
        super(TestFrame, self).__init__(width, height, order, buffer, root_point)

    def render(self, parent):
        bg = color.random_color()

        self.print(0, 0, "@", fg=(255-bg[0], 255-bg[1], 255-bg[2]), bg=bg)

        # do the super call last, since that's where the render-to-parent call happens.
        super().render(parent)

class FPSFrame(Frame):
    def __init__(self, width=7, height=1, order='F', buffer=None, root_point=Point2D(0, 0)):
        super().__init__(width, height, order, buffer, root_point)

        self.last_render_time = time.time()

    def render(self, parent):

        fps = int(1 / (time.time() - self.last_render_time))
        self.last_render_time = time.time()

        self.print(0, 0, str(fps), color.white)
        self.print(4, 0, "fps", color.white)
        super().render(parent)
