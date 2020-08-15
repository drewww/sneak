from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color

import math
from entity import Facing

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class WaitAction(Action):
    def perform(self) -> None:
        pass


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        # for any action with a direction, set the facing to the direction.
        # TODO strip this out. switch to failing an action with direction if it doesn't match facing.
        # self.entity.facing = Facing.get_direction(self.dx, self.dy)
        pass

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        super().perform()

        target = self.target_actor
        if not target:
            return  # No entity to attack.

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )

class ShootAction(ActionWithDirection):
    def perform(self) -> None:
        super().perform()

        target = self.target_actor
        if not target:
            return # No entity to attack.

        damage = 10

        self.engine.message_log.add_message(f'{self.entity.name.capitalize()} attacks {target.name} for {damage} hit points', color.white)

        target.fighter.hp -= damage

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        super().perform()

        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)

class RotateAction(Action):
    def __init__(self, entity: Actor, facing: Facing):
        super().__init__(entity)
        self.facing = facing

    def perform(self) -> None:
        print(f'updating {self.entity} facing to {self.facing}')
        self.entity.facing = self.facing

class TargetLockAction(Action):
    def __init__(self, entity: Actor, facing: Facing, target: Actor):
        super().__init__(entity)
        self.facing = facing
        self.target = target

    def perform(self) -> None:
        self.entity.facing = self.facing
        self.entity.target_lock = self.target

# this is practically only done by players. going to set facing auto on these.
class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        super().perform()

        self.entity.facing = Facing.get_direction(self.entity.x, self.entity.y, self.dx+self.entity.x, self.dy+self.entity.y)

        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
