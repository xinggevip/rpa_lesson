# -*- coding: utf-8 -*-
# time: 2024/8/8 21:32
# file: Captcha.py
# author: RPA高老师

import ddddocr


def alphanumeric_captcha(img_path, beta=False):
    '''
    图形数字验证码识别
    :param img_path: 验证码图片地址
    :param beta: False为老模型，True为新模型
    :return: 验证码识别结果
    '''

    ocr = ddddocr.DdddOcr(beta=beta)
    image = open(img_path, "rb").read()
    result = ocr.classification(image)

    return result


if __name__ == '__main__':
    img_path_1 = r'E:\project\myself\python\rpa\lesson02遇到各种验证码怎么办\英文数字验证码1.png'
    res_1 = alphanumeric_captcha(img_path_1)
    print(res_1)

    img_path_2 = r'E:\project\myself\python\rpa\lesson02遇到各种验证码怎么办\英文数字验证码2.jpeg'
    res_2 = alphanumeric_captcha(img_path_2)
    print(res_2)
    pass
