#!/usr/bin/env python3
import copy
import logging

import tcod

import color
import engine
from engineold import EngineOld
import entity_factories
from geometry import Point2D
from procgen import generate_dungeon


def main() -> None:
    screen_width = 160
    screen_height = 100

    logger = logging.getLogger("sneak")
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # TODO figure out how to make the time less verbose. don't need date.
    formatter = logging.Formatter('[%(levelname)s]\t(%(asctime)s)\t%(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    logger.info("Starting up.")

    e = engine.Engine(screen_width, screen_height, "sneak")


if __name__ == "__main__":
    main()
