import requests
from Common.handle_data import EnvData
"""
requests实现cookies鉴权
"""
login_url = "http://elm.cangdu.org/admin/login"
login_data = {"user_name":"admin","password":"123456"}
resp =requests.post(url=login_url, json=login_data)
print(resp.json())
# 主动获取cookies
cookie = resp.cookies
print("获取登录后的cookies",cookie)
setattr(EnvData,"cookie",cookie)

addshop_url = "https://elm.cangdu.org/shopping/addshop"
addshop_data = {"name":"元气森林","address":"广东省广州市天河区44","latitude":23.120422,"longitude":113.36217,"description":"","phone":15778451277,"promotion_info":"","float_delivery_fee":0,"float_minimum_order_amount":20,"is_premium":"","delivery_mode":"","new":"","bao":"","zhun":"","piao":"","startTime":"","endTime":"","image_path":"1781eecb5f288254.jpg","business_license_image":"1781ee551e888252.png","catering_service_license_image":"","activities":[],"category":"快餐便当/简餐"}
resp = requests.post(url=addshop_url,json=addshop_data,cookies=EnvData.cookie)
print(resp.json())







