# -*- coding: utf-8 -*-
# time: 2024/8/8 21:32
# file: Captcha.py
# author: RPA高老师

import ddddocr

def alphanumeric_captcha(img_path, beta=False):
    '''
    英文数字验证码识别
    :param img_path: 验证码图片地址
    :param beta: False为老模型，True为新模型
    :return: 验证码识别结果
    '''

    ocr = ddddocr.DdddOcr(beta=beta)
    image = open(img_path, "rb").read()
    result = ocr.classification(image)

    return result

def calc_distance(full_bg_path, cut_bg_path):
    '''
    滑块验证码识别
    '''
    slide = ddddocr.DdddOcr(det=False, ocr=False)

    with open(cut_bg_path, 'rb') as f:
        target_bytes = f.read()

    with open(full_bg_path, 'rb') as f:
        background_bytes = f.read()

    res = slide.slide_comparison(target_bytes, background_bytes)

    return res["target"][0]

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
    # img_path_1 = r'E:\project\myself\rpa\uibot\github\rpa_lesson\lesson02遇到各种图形验证码怎么办？\uibot源码\lesson02遇到各种验证码怎么办\res\data\英文数字验证码1.png'
    # res = alphanumeric_captcha(img_path_1)
    # print(res)

    full_bg_path = r'E:\project\myself\rpa\uibot\github\rpa_lesson\lesson02遇到各种图形验证码怎么办？\uibot源码\lesson02遇到各种验证码怎么办\res\data\01滑块验证码完整背景图.png'
    cut_bg_path = r'E:\project\myself\rpa\uibot\github\rpa_lesson\lesson02遇到各种图形验证码怎么办？\uibot源码\lesson02遇到各种验证码怎么办\res\data\02滑块验证码带缺口背景图.png'
    res = calc_distance(full_bg_path, cut_bg_path)
    print(res)

    pass
