# -*- coding:utf-8 -*-

import sys
import time
from PIL import Image, ImageOps
import numpy as np
import util.logger as logger
from stick_sdk import Stick


def write(stick, im, lines):
    len_ = Stick.LED_HEIGHT
    # im = im.resize((lines, len_), Image.BICUBIC)
    size = lines, len_
    im.thumbnail(size)
    px = np.array(im)
    # logger.d('px type = {}, shape = {}'.format(type(px), px.shape))
    # logger.d('im size = ({}, {})'.format(im.width, im.height))
    for x in range(im.width):
        pattern = [0] * (len_ * 3)
        for y in range(im.height):
            try:
                r, g, b = get_led_rgb(px[x, y])
                pattern[y * 3] = r
                pattern[y * 3 + 1] = g
                pattern[y * 3 + 2] = b
            except Exception:
                # logger.e('x={}, y={}'.format(x, y, r, g, b))
                raise
        stick.write(x, pattern)
        logger.d('write pattern line={}, pattern={}'.format(x, pattern))


def get_led_rgb((r, g, b)):
    k = Stick.LED_FACTOR
    return int(r / k), \
        int(g / k), \
        int(b / k)


def show(stick, lines):
    logger.d('show lines({})'.format(lines))
    while True:
        try:
            a = stick.accel()
            line = (a[1] + 0x8000) * lines / 0x10000
            logger.d('accel = {}, line = {}'.format(a, line))
            stick.show(line)

            time.sleep(0.1)

        except KeyboardInterrupt:
            break

        except Exception:
            raise


if __name__ == '__main__':
    file = sys.argv[1]
    im = Image.open(file).convert('RGB')

    s = Stick()
    s.init_sdk()
    s.stop_demo()

    im = ImageOps.mirror(im)
    lines = Stick.LED_WIDTH
    lines = int(round(im.height / Stick.LED_HEIGHT))
    logger.d('writing image...')
    write(s, im, lines)
    logger.d('complete!')
    show(s, lines)
