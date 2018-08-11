# -*- coding:utf-8 -*-

import sys
import time
from PIL import Image, ImageOps
import numpy as np
import util.logger as logger
from stick_sdk import Stick


def write(stick, im, lines):
    len_ = Stick.LED_HEIGHT
    im = im.resize((lines, len_))
    px = np.array(im)
    # px = np.array(im).transpose((1, 0, 2))          # change array pos
    px = px // Stick.LED_FACTOR * Stick.LED_FACTOR  # down color
    logger.d('px type={}, shape={}'.format(type(px), px.shape))
    for x in range(im.width):
        pattern = [0] * (len_ * 3)
        for y in range(im.height):
            try:
                r, g, b = px[y, x]
                pattern[y * 3] = int(r)
                pattern[y * 3 + 1] = int(g)
                pattern[y * 3 + 2] = int(b)
            except Exception:
                logger.e('x={}, y={}'.format(x, y))
                raise
        # pattern = np.ravel(px[x])
        stick.write(x, pattern)


def show(stick, lines):
    logger.d('show lines({})'.format(lines))
    while True:
        try:
            a = stick.accel()
            line = (a[1] + 0x8000) * lines / 0x10000
            stick.show(line)
            time.sleep(0.0001)

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
    # lines = int(round(im.height / Stick.LED_HEIGHT))
    logger.d('writing image...')
    write(s, im, lines)
    logger.d('complete!')
    show(s, lines)
