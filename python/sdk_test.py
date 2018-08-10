# -*- coding:utf-8 -*-

import time
import util.logger as logger
from stick_sdk import Stick
from stick_sdk_t import STICK

if __name__ == '__main__':
    s = Stick()
    s.init_sdk()
    s.stop_demo()

    h = 32
    s.write(0, [0x000000 for _ in range(h)])
    s.write(1, [0xff0000 for _ in range(h)])
    s.write(2, [0x00ff00 for _ in range(h)])
    s.write(3, [0x0000ff for _ in range(h)])
    s.write(4, [0xffff00 for _ in range(h)])
    s.write(5, [0xff00ff for _ in range(h)])
    s.write(6, [0x00ffff for _ in range(h)])
    s.write(7, [0xffffff for _ in range(h)])

    while True:
        try:
            accel = s.accel()
            gyro = s.gyro()
            logger.d('get accel = ({},{},{})'.format(accel[0], accel[1], accel[2]))
            logger.d('get gyro = ({},{},{})'.format(gyro[0], gyro[1], gyro[2]))

            line = (accel[1] + 0x8000) * 7 / 0x10000
            s.show(line)
            logger.d('show line={}'.format(line))

            time.sleep(0.2)

        except KeyboardInterrupt:
            break

        except Exception:
            raise
