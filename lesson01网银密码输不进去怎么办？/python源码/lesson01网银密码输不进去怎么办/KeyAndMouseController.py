# -*- coding: utf-8 -*-
# time: 2024/8/4 14:17
# file: KeyAndMouseController.py
# author: RPA高老师

import sys
import traceback

import win32com.client
from ctypes import *

import win32api, win32gui, win32con
import time
from enum import Enum


class Lan(Enum):
    """
    语言代码值参考：https://msdn.microsoft.com/en-us/library/cc233982.aspx
    """
    EN = 0x4090409
    ZH = 0x8040804

def change_lan(lan: Lan):
    """
    修改当前激活窗口输入法
    :param lan: 语言类型
    :return: True 修改成功，False 修改失败
    """
    # 获取系统输入法列表
    hwnd = win32gui.GetForegroundWindow()
    im_list = win32api.GetKeyboardLayoutList()
    im_list = list(map(hex, im_list))

    # 加载输入法
    if hex(lan.value) not in im_list:
        win32api.LoadKeyboardLayout('0000' + hex(lan.value)[-4:], 1)

    result = win32api.SendMessage(
        hwnd,
        win32con.WM_INPUTLANGCHANGEREQUEST,
        0,
        lan.value)
    print(result)
    if result == 0:
        print('设置%s键盘成功！' % lan.name)
    else:
        raise Exception("设置键盘英文状态失败")
    return result == 0


def get_vmkey_obj():
    '''
    获取无涯键鼠盒子对象
    :return:
    '''
    # 进程内注册插件,模块所在的路径按照实际位置修改
    hkmdll = windll.LoadLibrary(r"F:\document\soft\无涯键鼠盒子\无涯键鼠盒子配套软件(20240227)(hkm5.70_cp2.07)\无涯键鼠盒子模块\标准版\64位模块\wyhkm.dll")
    hkmdll.DllInstall.argtypes = (c_long, c_longlong)
    if hkmdll.DllInstall(1, 2) < 0:
        print("注册失败!")
        sys.exit(0)

    # 创建对象
    try:
        wyhkm = win32com.client.Dispatch("wyp.hkm")
    except:
        print("创建对象失败!")
        sys.exit(0)
    # 获得模块版本号
    version = wyhkm.GetVersion()
    print("无涯键鼠盒子模块版本：" + hex(version))
    # 查找设备,这个只是例子,参数中的VID和PID要改成实际值
    DevId = wyhkm.SearchDevice(0x2612, 0x1701, 0)
    if DevId == -1:
        print("未找到无涯键鼠盒子")
        sys.exit(0)

    # 打开设备,DPI模式取每个显示器DPI感知
    if not wyhkm.Open(DevId, 0):
        print("打开无涯键鼠盒子失败")
        sys.exit(0)

    return wyhkm


def vm_input(keyword):
    wyhkm = get_vmkey_obj()
    try:
        wyhkm.DelayRnd(500, 1000)
        # 首先切换到英文输入法状态
        change_lan(Lan.EN)
        wyhkm.DelayRnd(1000, 2000)

        for item in keyword:
            item_is_upper = item.isupper()
            if item_is_upper:
                wyhkm.KeyDown("Shift")
            if item == '!':
                wyhkm.KeyPress("Shift + 1")

            wyhkm.KeyPress(item)
            if item_is_upper:
                wyhkm.KeyUp("Shift")

            wyhkm.DelayRnd(200, 500)

        # x = 0
        # y = 0
        # r = wyhkm.GetCursorPos(x, y)
        # print(str(x) + "," + str(y))
        # print(len(r))
        # print(r)
        # print(wyhkm.CheckPressedKeys(0))
    except Exception as err:
        traceback.print_exc()  # 直接输出
        # 关闭设备
        wyhkm.Close()


def mouse_tuo(x):
    '''
    从当前位置横坐标移动
    :param x:
    :return:
    '''
    wyhkm = get_vmkey_obj()

    try:
        time.sleep(3)
        wyhkm.LeftDown()
        wyhkm.MoveRP(x, 0)
        wyhkm.LeftUp()
        pass

    except Exception as err:
        traceback.print_exc()  # 直接输出
        # 关闭设备
        wyhkm.Close()


if __name__ == '__main__':
    keyword = "1234"
    vm_input(keyword)
    # mouse_tuo(50)

