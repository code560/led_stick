# -*- coding:utf-8 -*-

import sys
import time
from PIL import Image, ImageOps
import numpy as np
import util.logger as logger
from stick_sdk import Stick


def write(stick, im, lines):
    len_ = 32
    im = im.resize((lines, len_), Image.BICUBIC)
    px = np.array(im)
    for x in range(im.width):
        pattern = [0] * len_
        for y in range(im.height):
            r, g, b = get_led_rgb(px[x, y])
            pattern[y * 3] = r
            pattern[y * 3 + 1] = g
            pattern[y * 3 + 2] = b
        stick.write(x, pattern)


def get_led_rgb(r, g, b):
    k = Stick.LED_FACTOR
    return int(r / k), \
        int(g / k), \
        int(b / k)


def show(stick, lines):
    while True:
        try:
            a = stick.get_accel()
            line = (a[1] + 0x8000) * lines / 0x10000
            stick.show(line)

            time.sleep(0.1)

        except KeyboardInterrupt:
            break

        except Exception:
            raise


if __name__ == '__main__':
    file = sys.argv[1]
    im = Image.open(file)

    s = Stick()
    s.init_sdk()
    s.stop_demo()

    im = ImageOps.mirror(im)
    lines = 1364
    logger.d('writing image...')
    write(s, im, lines)
    logger.d('complete!')
    show(s, lines)
