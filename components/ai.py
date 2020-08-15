from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod

from actions import Action, MeleeAction, MovementAction, WaitAction
from components.base_component import BaseComponent

from entity import Facing

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action, BaseComponent):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def __str__(self):
        return f'HostileEnemy({self.entity.x}, {self.entity.y})'

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        # wow this is a cheap trick. If the human can see me, then I act.
        # this is where the logic around ambient pathing goes, TBD.

        # for now, what needs to happen is we need to know if there's a current
        # uninterrupted sightline between the hostile and the player.
        # if yes, check if we're facing. if we are, fire. otherwise, rotate.
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:

            visibility = tcod.map.compute_fov(
                self.engine.game_map.tiles["transparent"], (self.entity.x, self.entity.y))

            target_is_visible = visibility[target.x, target.y]
            print(f'{self} -> ({target.x}, {target.y}) = {target_is_visible}')

            if target_is_visible:
                if distance <= 1:
                    print(f'too close to attack!')
                    # return MeleeAction(self.entity, dx, dy).perform()
                if distance > 1:
                    # oh actually, this is easy! get angle,
                    # check if it collapses to facing. done.
                    firing_direction = Facing.get_direction(self.entity.x, self.entity.y, target.x, target.y)
                    print(f'firing_facing: {firing_direction} + my_facing: {self.entity.facing}')

            else:
                self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()
