#!/usr/bin/env python3
import copy

import tcod

import color
from engine import Engine
import entity_factories
from procgen import generate_dungeon


def main() -> None:
    screen_width = 160
    screen_height = 100

    map_width = 160
    map_height = 86

    room_max_size = 30
    room_min_size = 15
    max_rooms = 10

    max_monsters_per_room = 1

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)
    player.is_player = True

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine,
    )

    engine.update_fov()

    engine.message_log.add_message(
        "Begin the run.", color.welcome_text
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="sneak",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            engine.render(root_console)

            engine.event_handler.handle_events(context)



if __name__ == "__main__":
    main()
