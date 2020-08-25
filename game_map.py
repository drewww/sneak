from __future__ import annotations

import logging
from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

import tile_types
from entity import Actor
from frame import Frame

logger = logging.getLogger("sneak")


if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine


class GameMap (Frame):
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        super().__init__(width, height)

        self.engine = engine

        self.entities = set(entities)
        self.map_tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=True, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=True, order="F"
        )  # Tiles the player has seen before

        # self.vision_mode = False
        # self.vision_row=0

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

    def render(self, parent: Frame) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """

        # entities_sorted_for_rendering = sorted(
        #     self.entities, key=lambda x: x.render_order.value
        # )

        tiles_to_update = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.map_tiles["light"], self.map_tiles["dark"]],
            default=tile_types.SHROUD,
        )

        # self.tiles_rgb[0 : self.width, self.vision_row : self.height] = self.map_tiles[0:self.width,self.vision_row:self.height]
        self.tiles_rgb[0 : self.width, 0 : self.height] = tiles_to_update[0:self.width,0:self.height]

        super().render(parent)

