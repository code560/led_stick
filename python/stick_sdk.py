# -*-coding:utf-8-*-

import os
from ctypes import *


class Stick():
    LED_FACTOR = 63.759

    dirname = os.path.dirname(__file__)
    dirname = os.path.abspath(os.path.join(dirname, '..'))
    lib = dirname + '/lib/stick_sdk.so'

    def __init__(self):
        self.lib = cdll.LoadLibrary(Stick.lib)
        self.init_sdk()

    def init_sdk(self):
        return self.lib.init_sdk() != 0

    def stop_demo(self):
        self.lib.stop_led_demo()

    # line(int): 0 - 1364
    # pattern(char): 32 * 3(RGB)
    def write(self, line, pattern):
        size = len(pattern)
        array = []
        for color in pattern:
            array.extend(self.__get_led_rgb(color))
        carray = c_byte * len(array)
        cpattern = carray(*array)
        self.lib.write_line(line, cpattern)

    def __get_led_rgb(self, color):
        k = Stick.LED_FACTOR
        r = int(((color & 0xff0000) >> 16) / k)
        g = int(((color & 0x00ff00) >> 8) / k)
        b = int((color & 0x0000ff) / k)
        return r, g, b

    # line(int): 0 - 1364
    def show(self, line):
        self.lib.show_line(line)

    # return(ushort): x, y, z
    def accel(self):
        val = self.__carray(3)
        self.lib.get_accel(val)
        return tuple(val)

    def gyro(self):
        val = self.__carray(3)
        self.lib.get_gyro(val)
        return tuple(val)

    def __carray(self, size):
        carray = c_short * size
        array = [0] * size
        return carray(*array)
