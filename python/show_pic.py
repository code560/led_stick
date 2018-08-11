# -*- coding:utf-8 -*-

import sys
import time
from PIL import Image, ImageOps
import numpy as np
import util.logger as logger
from stick_sdk import Stick


def write(stick, im, lines):
    len_ = Stick.LED_HEIGHT # led
    size = lines, len_      # led map size for FPGA
    im = im.resize(size)
    px = np.array(im)
    px = px // Stick.LED_FACTOR * Stick.LED_FACTOR
    for x in range(im.width):
        pattern = [0] * (len_ * 3)
        for y in range(im.height):
            try:
                # r, g, b = get_led_rgb(px[y, x])
                r, g, b = int(px[x])
                pattern[y * 3] = r
                pattern[y * 3 + 1] = g
                pattern[y * 3 + 2] = b
            except Exception:
                logger.e('x={}, y={}'.format(x, y, r))
                raise
        # pattern = np.ravel(px[x])
        stick.write(x, pattern)


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
