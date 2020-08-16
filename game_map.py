from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console
import tcod

from entity import Actor, Facing
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int,
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:

            # for now, always render all enemies. this will make my life easier.
            # if self.visible[entity.x, entity.y]:
            console.print(
                x=entity.x, y=entity.y, string=entity.char, fg=entity.color
            )

            # now print their facing
            # not sure where to do this but need to map facing to dx/dy.

            LASER_SIGHT_DISTANCE = 4

            # if we're target locked, don't draw facing, draw direct connection
            if not entity.is_player and entity.target_lock == None:
                (fx, fy) = Facing.get_pos(entity.facing)

                # get delta to destination
                (dx, dy) = (LASER_SIGHT_DISTANCE*fx, LASER_SIGHT_DISTANCE*fy)

                cells = tcod.los.bresenham((entity.x, entity.y),
                    (entity.x + dx, entity.y + dy))

                cells = np.delete(cells, 0, 0)

                discount = 0.5
                for cell in cells:
                    tile = self.tiles[cell[0]][cell[1]]

                    if tile['walkable'] or tile['transparent']:
                        console.print(cell[0], cell[1], string=' ', bg=(int(255*discount), 0, 0))
                        discount -= 0.5/LASER_SIGHT_DISTANCE
            elif not entity.is_player and entity.target_lock != None:
                cells = tcod.los.bresenham((entity.x, entity.y),
                    (entity.target_lock.x, entity.target_lock.y))

                cells = np.delete(cells, 0, 0)

                for cell in cells:
                    tile = self.tiles[cell[0]][cell[1]]

                    if tile['walkable'] or tile['transparent']:
                        console.print(cell[0], cell[1], string=' ', bg=(int(255), 0, 0))


            # console.print(x=entity.x+fx, y=entity.y+fy, string='*', fg=entity.color)
