import requests
import base64
from PIL import Image  # 用于打开图片和对图片处理
from pytesseract import image_to_string, pytesseract  # 用于图片转文字
pytesseract.tesseract_cmd = 'D:\\Program Files\\Tesseract-OCR\\tesseract'


# 空白背景色 pytesseract无法识别，更换一下背景色
def change_background(img_fg):
    try:
        img = Image.open(img_fg)
        x,y = img.size
        new_img = Image.new("RGBA",img.size,(255,255,255))
        new_img.paste(img,(0,0,x,y),img)
        return new_img
    except:
        print("更换图片背景失败")

# 识别图片验证码
def ocr2str(img):
    return str(image_to_string(img))


# 请求图片验证码接口
code_url = "https://elm.cangdu.org/v1/captchas"
code_resp = requests.post(code_url)
print(code_resp.json())

"""
data:image/xxx;base64的图片编码数据转化为真正的图片
"""
img_imf = code_resp.json()["code"].split(",")[1]
page_content = base64.b64decode(img_imf)
print(page_content)

# 保存图片验证码
with open("code.png","wb") as f:
    f.write(page_content)

# 验证码
code = ocr2str("code.png")
print(code)








