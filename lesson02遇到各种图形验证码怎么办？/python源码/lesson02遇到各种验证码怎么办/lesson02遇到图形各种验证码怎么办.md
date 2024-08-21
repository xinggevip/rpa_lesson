# lesson02遇到各种图形验证码怎么办

作者：RPA高老师

日期：2024-08-21

## 描述
登录过程中往往会遇到各种各样的验证码，让RPA机器人自动识别验证码成为了RPA开发者的必备技能

## 验证码识别原理
常见的图形验证码有英文数字验证码、 滑块验证码、点选验证码。使用人工智能及OCR技术识别验证码，简单的验证码网上有开源项目可以解决如ddddocr，复杂的验证码有专业的服务商如图鉴、超级鹰

## 注意事项
要在符合法律法规及道德规范下谨慎使用该技术,不得用于非法用途或侵犯他人权益的行为

## 验证码识别
### 英文数字验证码
这种验证码最常见，也最容以识别，用开源项目DDDDOCR即可识别
github开源地址：https://github.com/sml2h3/ddddocr

安装命令：
```
pip install opencv-python -i https://pypi.mirrors.ustc.edu.cn/simple some-package --target="RPA项目python目录"
pip install ddddocr -i https://pypi.mirrors.ustc.edu.cn/simple some-package --target="RPA项目python目录"
```

### 滑块验证码

### 点选验证码