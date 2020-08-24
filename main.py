#!/usr/bin/env python3
import logging

import engine


def main() -> None:
    screen_width = 80
    screen_height = 50

    logger = logging.getLogger("sneak")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # TODO figure out how to make the time less verbose. don't need date.
    formatter = logging.Formatter('[%(levelname)s]\t(%(asctime)s)\t%(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    logger.info("Starting up.")

    e = engine.Engine(screen_width, screen_height, "sneak")


if __name__ == "__main__":
    main()
