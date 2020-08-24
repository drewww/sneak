#!/usr/bin/env python3
import copy

import tcod

import color
from engine import Engine
from engineold import EngineOld
import entity_factories
from procgen import generate_dungeon


def main() -> None:
    screen_width = 160
    screen_height = 100

    e = Engine(screen_width, screen_height, "sneak")


if __name__ == "__main__":
    main()
