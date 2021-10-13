

import requests
from Common.handle_log import logger
from Common.handle_config import conf



class HandleRequests:
    def __init__(self):
        """session管理器"""
        self.session = requests.session()

    def send_requests(self, method, url, params=None, data=None, json=None, files=None,headers=None,**kwargs):
        logger.info("发起一次HTTP请求")
        url = self.pre_url(url)
        logger.info("请求方法为：{}".format(method))
        logger.info("请求url为：{}".format(url))
        if params:
            params = self.pre_data(params)
            logger.info("请求数据为：{}".format(params))
        elif data:
            data = self.pre_data(data)
            logger.info("请求数据为：{}".format(data))
        elif json:
            json = self.pre_data(json)
            logger.info("请求数据为：{}".format(json))


        method = method.upper()
        resp = self.session.request(method, url, params=params, data=data, json=json, files=files, headers=headers,**kwargs)
        logger.info("响应状态码：{}".format(resp.status_code))
        logger.info("响应数据为：{}".format(resp.json()))
        return resp

    def close_session(self):
        """关闭session"""
        self.session.close()

    def pre_url(self,url):
        base_url = conf.get("server", "base_url")
        if url.startswith("/"):
            return base_url + url
        else:
            return base_url + "/" + url


    def pre_data(self,data):
        """
        如果data是字符串，则转换成字典对象
        :param data:
        :return:
        """
        if data is not None and isinstance(data, str):
            if data.find("null") != -1:
                data = data.replace("null", "none")
            data = eval(data)
        return data

    def upLoadImages(self,file_path,filename):
        files = {"file":(filename,open(file_path,"rb"),'image/jpeg')}

        return files




req = HandleRequests()



# if __name__ == '__main__':
#     # 以下是测试代码
#     # post请求接口
#     login_url = "http://elm.cangdu.org/admin/login"
#     login_data = {"user_name": "admin", "password": "123456"}
#     req = HandleRequests()
#     resp = req.send_requests("post", url=login_url, data=login_data)
#     cookies = resp.cookies
#     addshop_url = "https://elm.cangdu.org/shopping/addshop"
#     addshop_data = {"name": "阿甘锅盖787", "address": "广东省广州市天河区44", "latitude": 23.120422, "longitude": 113.36217,
#                     "description": "", "phone": 15778451277, "promotion_info": "", "float_delivery_fee": 0,
#                     "float_minimum_order_amount": 20, "is_premium": "", "delivery_mode": "", "new": "", "bao": "",
#                     "zhun": "", "piao": "", "startTime": "", "endTime": "", "image_path": "1781eecb5f288254.jpg",
#                     "business_license_image": "1781ee551e888252.png", "catering_service_license_image": "",
#                     "activities": [], "category": "快餐便当/简餐"}
#     resp = req.send_requests("post", url=addshop_url, data=addshop_data, cookies=cookies)

