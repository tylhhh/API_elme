from PIL import Image  # 用于打开图片和对图片处理
import pytesseract  # 用于图片转文字
import requests,base64


class VerificationCode:
    def __init__(self,code_url):
        self.code_url = code_url

    # 获取验证码图片
    def get_pictures(self):
        code_resp = requests.post(self.code_url) # 请求图片验证码接口
        data = code_resp.json()["code"].split(",")[1]  # 获取data:image/xxx;base64后面的编码值
        img_content = base64.b64decode(data)  # 图片编码数据转化成真正的图片
        img = open("code.png","wb")
        img.write(img_content)
        #
        # with open("code.png","wb") as f:  # 保存图片验证码
        #     f.write(img_content)
        return img

    # 首先用convert把图片转成黑白色，设置threshold阈值，超过阈值的为黑色
    def processing_image(self):
        image_obj = self.get_pictures()  # 获取验证码
        img = image_obj.convert("L")  # 转灰度
        pixdata = img.load()
        w, h = img.size
        threshold = 160  # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
        # 遍历所有像素，大于阈值的为黑色
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < threshold:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return img






if __name__ == '__main__':
    code_url = "https://elm.cangdu.org/v1/captchas"
    v = VerificationCode(code_url)
    v.get_pictures()
    print(v.get_pictures())
    # print(v.processing_image())




