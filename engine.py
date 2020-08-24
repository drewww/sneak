import logging

import tcod

from input_handler import EventHandler

logger = logging.getLogger("sneak")


class Engine:
    def __init__(self, screen_width: int, screen_height: int, title: str):

        tileset = tcod.tileset.load_tilesheet(
            "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        )

        logger.debug(f'Loaded tileset: {tileset}')

        with tcod.context.new_terminal(
                screen_width,
                screen_height,
                tileset=tileset,
                title=title,
                vsync=True,
        ) as context:
            self.root_console = tcod.Console(screen_width, screen_height, order="F")
            self.event_handler = EventHandler()

            while True:
                # logger.debug("game loop start")
                self.root_console.clear()
                context.present(self.root_console)

                self.render()
                self.handle_events(context)

    def render(self):
        pass

    def handle_events(self, context):
        for ev in tcod.event.get():
            logger.debug(f'handling ev: {ev}')
            self.event_handler.handle_event(context, ev)

