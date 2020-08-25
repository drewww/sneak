import logging

import tcod

from frame import Frame, TestFrame, FPSFrame
from geometry import Point2D
from input_handler import EventHandler
from procgen import generate_map

logger = logging.getLogger("sneak")


class Engine:
    def __init__(self, screen_width: int, screen_height: int, title: str):

        tileset = tcod.tileset.load_tilesheet(
            "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        )

        logger.debug(f'Loaded tileset: {tileset}')

        self.screen_width = screen_width
        self.screen_height = screen_height

        # TODO understand more deeply why this is a thing
        with tcod.context.new_terminal(
                screen_width,
                screen_height,
                tileset=tileset,
                title=title,
                vsync=True,
        ) as context:
            self.root_console = Frame(screen_width, screen_height, order="F")

            self.event_handler = EventHandler(self)
            self.map = generate_map(10, 5, 20, self.root_console.width, self.root_console.height, 0, self)

            fps_frame = FPSFrame()
            fps_frame.z_index = 1
            self.map.z_index = -500

            self.root_console.add_child(fps_frame)
            self.root_console.add_child(self.map)


            while True:
                # logger.debug("game loop start")
                self.root_console.clear()

                self.handle_events(context)
                self.render()

                context.present(self.root_console)


    def render(self):
        self.root_console.render()

    def handle_events(self, context):
        for ev in tcod.event.get():
            # logger.debug(f'handling ev: {ev}')
            self.event_handler.handle_event(context, ev)

    def add_random_frame(self):
        new_frame = TestFrame(root_point=Point2D.rand(max_point=Point2D(self.screen_width, self.screen_height)))

        logging.info(f"Adding random frame: {new_frame}")

        self.root_console.add_child(new_frame)


# TODO abstract out to SneakEngine and keep Engine clean.