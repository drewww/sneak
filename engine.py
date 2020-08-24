import tcod

from input_handler import EventHandler


class Engine:
    def __init__(self, screen_width:int, screen_height:int, title:str):

        tileset = tcod.tileset.load_tilesheet(
            "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        )

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
                self.root_console.clear()
                context.present(self.root_console)

                self.render()
                self.handle_events()

                self.event_handler.handle_events(context)
                # self.event_handler.on_render(console=root_console)
                # self.event_handler.handle_events(context)

    def render(self):
        pass

    def handle_events(self):
        pass
