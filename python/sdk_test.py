# -*- coding:utf-8 -*-

import time
import util.logger as logger
from stick_sdk import Stick
from stick_sdk_t import STICK

if __name__ == '__main__':
    s = Stick()
    # s.init_sdk()
    # s.stop_demo()

    t = STICK
    t.init_sdk()
    t.stop_led_demo()

    while True:
        try:
            # accel = s.accel()
            # gyro = s.gyro()
            accel = t.get_accel()
            gyro = t.get_gyro()
            logger.d('get accel = ({},{},{})'.format(accel[0], accel[1], accel[2]))
            logger.d('get gyro = ({},{},{})'.format(gyro[0], gyro[1], gyro[2]))

            time.sleep(0.2)

        except KeyboardInterrupt:
            break

        except Exception:
            raise
