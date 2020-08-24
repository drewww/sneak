import logging
from typing import Optional

import tcod

from actions import Action

logger = logging.getLogger("sneak")


class EventHandler(tcod.event.EventDispatch[Action]):

    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            self.dispatch(event)

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        logger.debug(event)
        pass
        # if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
        #     self.engine.mouse_location = event.tile.x, event.tile.y

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def on_render(self, console: tcod.Console) -> None:
        pass
        # self.engine.render(console)
