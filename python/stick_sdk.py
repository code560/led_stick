# -*-coding:utf-8-*-

from ctypes import *
import util.logger as logger


class Stick():

    def __init__(self):
        self.lib = cdll.LoadLibrary('../lib/stick_sdk.so')

    def init_sdk(self):
        return self.lib.init_sdk() != 0

    def stop_demo(self):
        self.lib.stop_led_demo()

    # line(int): 0 - 1364
    # pattern(char): 32 * 3(RGB)
    def write(self, line, pattern):
        self.lib.write_line(line, pattern)

    # line(int): 0 - 1364
    def show(self, line):
        self.lib.show_line(line)

    # return(ushort): x, y, z
    def accel(self):
        # val = Triaxial()
        # self.lib.get_accel(ctypes.byref(val))
        # logger.d('get accel= ({},{},{})'.format(val.x, val.y, val.z))
        # return val.x, val.y, val.z

        get_accel = self.lib.get_accel
        get_accel.argtypes = [POINTER(c_ushort)]
        array = POINTER(c_ushort)
        val = array()
        get_accel(byref(val))
        logger.d('get accel = ({},{},{})'.format(val[0], val[1], val[2]))
        return val

    def gyro(self):
        pass


class Triaxial(Structure):
    _axis_ = [
        ('x', c_ushort),
        ('y', c_ushort),
        ('z', c_ushort)]

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
