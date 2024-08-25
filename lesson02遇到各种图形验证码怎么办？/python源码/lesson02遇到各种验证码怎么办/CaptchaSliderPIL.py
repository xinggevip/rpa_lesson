# -*- coding: utf-8 -*-
# time: 2024/8/24 14:01
# file: CaptchaSliderPIL.py
# author: RPA高老师


import PIL.ImageChops as imagechops
from PIL import Image, ImageDraw

import time


def calc_distance(srcImg, distImg):
    '''
    滑块验证码生成拖动距离
    '''
    im1 = Image.open(srcImg)
    im2 = Image.open(distImg)
    # 得出两图不一致的地方
    diff = imagechops.difference(im1, im2)
    draw = ImageDraw.Draw(diff)
    # 通过颜色处理清除干扰块
    for x in range(0, 260):
        for y in range(0, 116):
            pixelColor = diff.getpixel((x, y))
            if pixelColor[0] >= 100 or pixelColor[1] >= 100 or pixelColor[2] >= 100:
                draw.line((x, y, x, y), (255, 255, 255, 255))
            else:
                draw.line((x, y, x, y), (0, 0, 0, 0))
    # #清理完可以show一下，查看清理完之后的黑白化效果
    # diff.show()
    # 找第一个块中的参照点
    firsetPoint = [0, 0]
    for x in range(0, 260):
        for y in range(0, 116):
            pixelColor = diff.getpixel((x, y))
            if pixelColor != (0, 0, 0, 0):
                firsetPoint = [x, y]
                break
        if firsetPoint != [0, 0]:
            break
    # 往后跳50找第二个块中的参照点，50是矩形宽度
    secondPoint = [0, 0]
    for x in range(firsetPoint[0] + 50, 260):
        for y in range(0, 116):
            pixelColor = diff.getpixel((x, y))
            if pixelColor != (0, 0, 0, 0):
                secondPoint = [x, y]
                break
        if secondPoint != [0, 0]:
            break
    # #画两条线看看位置是否标注正确，仅用于调试
    # draw.line((firsetPoint[0], firsetPoint[1], firsetPoint[0]+20, firsetPoint[1]),(6,255,9,0))
    # draw.line((secondPoint[0], secondPoint[1], secondPoint[0]+20, secondPoint[1]),(9,8,255,0))
    # diff.show()
    diffPixel = secondPoint[0] - firsetPoint[0]
    return diffPixel

def generate_tracks(S):
    '''
    生成移动轨迹
    '''
    S += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = S * 3 / 5  # 减速阀值
    while current < S:
        if current < mid:
            a = 2  # 加速度为+2
        else:
            a = -3  # 加速度-3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
    return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}


if __name__ == '__main__':
    srcImg = r'E:\project\myself\rpa\uibot\github\rpa_lesson\lesson02遇到各种图形验证码怎么办？\uibot源码\lesson02遇到各种验证码怎么办\res\data\01滑块验证码完整背景图.png'
    distImg = r'E:\project\myself\rpa\uibot\github\rpa_lesson\lesson02遇到各种图形验证码怎么办？\uibot源码\lesson02遇到各种验证码怎么办\res\data\02滑块验证码带缺口和缺块背景图.png'

    distance = calc_distance(srcImg, distImg)
    print(distance)

    time.sleep(3)


    pass