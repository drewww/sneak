from __future__ import annotations

import logging
from typing import Optional

import tcod

from actions import Action

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine import Engine

logger = logging.getLogger("sneak")

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_event(self, context: tcod.context.Context, ev: tcod.event.Event) -> None:
        # no idea what this does
        context.convert_event(ev)
        self.dispatch(ev)

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        # logger.debug(event)

        # TODO add this back in when we've updated game_map.
        # if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
        #     self.engine.mouse_location = event.tile.x, event.tile.y

        pass

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: "tcod.event.KeyDown") -> None:
        key = event.sym

        if key == tcod.event.K_TAB:
            logger.info('toggle vision mode')
            pass
        elif key == tcod.event.K_a:
            self.engine.add_random_frame()
        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()

    def ev_keyup(self, event: "tcod.event.KeyUp") -> None:
        pass
