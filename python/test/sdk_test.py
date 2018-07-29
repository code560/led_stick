# -*- coding:utf-8 -*-

import time
from ..stick_sdk import Stick


if __name__ == '__main__':
    s = Stick()
    s.init_sdk()

    while True:
        try:
            accel = s.accel()
            print('accel({})'.format(type(accel)))
            time.sleep(0.01)

        except KeyboardInterrupt:
            return

        except Exception:
            raise

