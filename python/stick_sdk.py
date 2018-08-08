# -*-coding:utf-8-*-

import os
from ctypes import *
import util.logger as logger


class Stick():

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
        carray = c_char * size
        array = [0 for i in range(size)]
        for color in pattern:
            array.append(self.__get_led_rgb(color))
        cpattern = carray(*array)
        self.lib.write_line(line, cpattern)

    def __get_led_rgb(self, color):
        k = 63.759
        r = int(((color & 0xff0000) >> 16) / k)
        g = int(((color & 0x00ff00) >> 8) / k)
        b = int((color & 0x0000ff) / k)
        return r,g,b

    # line(int): 0 - 1364
    def show(self, line):
        self.lib.show_line(line)

    # return(ushort): x, y, z
    def accel(self):
        val = self.__carray_ushort(3)
        self.lib.get_accel(val)
        logger.d('get accel = ({},{},{})'.format(val[0], val[1], val[2]))
        return tuple(val)

    def gyro(self):
        val = self.__carray_ushort(3)
        self.lib.get_gyro(val)
        logger.d('get gyro = ({},{},{})'.format(val[0], val[1], val[2]))
        return tuple(val)

    def __carray_ushort(self, size):
        carray = c_ushort * size
        array = [0 for i in range(size)]
        return carray(*array)

