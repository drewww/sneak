from __future__ import annotations

import copy, math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from render_order import RenderOrder
import tcod
import numpy as np

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from game_map_old import GameMap

T = TypeVar("T", bound="Entity")

from enum import auto, Enum
class Facing(Enum):
    NW = auto()
    N = auto()
    NE = auto()
    E = auto()
    SE = auto()
    S = auto()
    SW = auto()
    W = auto()

    @classmethod
    def get_pos(cls, f: Facing):
        map = {Facing.NW: (-1, -1), Facing.N: (0, -1), Facing.NE: (1, -1), Facing.E: (1, 0), Facing.SE: (1, 1), Facing.S: (0, 1), Facing.SW: (-1,1), Facing.W: (-1, 0)}
        return map[f]

    @classmethod
    def get_angle(cls, f: Facing):
        pos = cls.get_pos(f)
        return math.atan2(pos[0], pos[1])

    @classmethod
    def get_direction(cls,
        x1:int, y1:int,
        x2:int = 0, y2:int = 0):

        dx = x2-x1
        dy = y2-y1

        # this angle is in radians
        # 0 = up, 1=right
        angle = math.atan2(dy, dx)

        # i want to map this down to 0/1/-1 on two axes.
        # or maybe I'm just weak and do the map version.
        # these = are a little shaky and I'm not sure they're mutually exclusive
        if angle <= math.pi/8 and angle > -math.pi/8:
            return Facing.E
        elif angle <= 3*math.pi/8 and angle > math.pi/8:
            return Facing.SE
        elif angle <= 5*math.pi/8 and angle > 3*math.pi/8:
            return Facing.S
        elif angle <= 7*math.pi/8 and angle > 5*math.pi/8:
            return Facing.SW
        elif angle >= 7*math.pi/8 or angle < -7*math.pi/8:
            return Facing.W
        elif angle >= -3*math.pi/8 and angle < -math.pi/8:
            return Facing.NE
        elif angle >= -5*math.pi/8 and angle < -3*math.pi/8:
            return Facing.N
        elif angle >= -7*math.pi/8 and angle < -5*math.pi/8:
            return Facing.NW



class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    gamemap: GameMap

    def __init__(
        self,
        gamemap: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        facing: Facing = Facing.N,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.facing = facing
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if gamemap:
            # If gamemap isn't provided now then it will be set later.
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def __str__(self):
        return f'({self.name}: ({self.x}, {self.y}):{self.facing})'

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entitiy at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "gamemap"):  # Possibly uninitialized.
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        fighter: Fighter,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.is_player = False

        self.fighter = fighter
        self.fighter.entity = self

        # abstract into a hostile class? PC can't have a target lock i think?
        self.target_lock = None

    def get_visibility(self, tiles):
        visibility = tcod.map.compute_fov(
            tiles, (self.x, self.y), algorithm=1, radius=24)

        # now, whack it with a facing mask.
        # my meh idea for this is raytracing.

        # I think there's a one command way to do this but i'm lazy
        mask = np.full(tiles.shape, False)
        facing_angle = Facing.get_angle(self.facing)

        # I feel like there's a clever list comprehension here but...
        # ths is expensive. we only want to consider True values here
        # but I don't know how to back out from a tile to its coordinates.
        # this makes make think that ultimately tiles need unique ids not just be naked booleans?
        for x in range(0, visibility.shape[0]):
            for y in range(0, visibility.shape[1]):

                visible = visibility[x][y]
                if not visible:
                    continue

                # first, compute the distance to the entity.
                # then compute the angle.
                # then set true/false based on the acceptable range for that angle.

                # could do this fancy with pathfinder/djikstra but fuck it, pythagoras had this worked out fine.
                distance = int(math.sqrt(math.pow(self.x-x, 2) + math.pow(self.y-y, 2)))

                angle = math.atan2(self.x-x, self.y-y) + math.pi
                angle_distance = min(abs(angle-facing_angle),
                                         2*math.pi - (angle-facing_angle))

                if(angle_distance < math.pi/4):
                    r = 24
                elif(angle_distance < math.pi/2):
                    r = 6
                else:
                    r = 2

                # flip it to False if it's out of range for the angle.
                if distance > r:
                    visibility[x][y] = False

        return visibility

    # this is an odd way to do this. probably fine, but this was the side-effecting problem with setting AI to null.
    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
