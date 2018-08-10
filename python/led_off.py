# -*- coding:utf-8 -*-

from stick_sdk import Stick

if __name__ == '__main__':
    s = Stick()
    s.init_sdk()
    s.stop_demo()

    s.write(0, [0] * 32)
    s.show(0)
