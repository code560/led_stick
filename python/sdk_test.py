# -*- coding:utf-8 -*-

import time
from stick_sdk import Stick


if __name__ == '__main__':
    s = Stick()
    s.init_sdk()
    s.stop_demo()

    while True:
        try:
            accel = s.accel()
            gyro = s.gyro()
            time.sleep(0.2)

        except KeyboardInterrupt:
            break

        except Exception:
            raise
