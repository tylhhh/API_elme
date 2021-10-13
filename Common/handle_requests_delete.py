import requests,json
from Common.handle_config import conf
from Common.handle_log import logger


def send_requests(method, url, data=None):
    logger.info("发起一次http请求")
    url = pre_url(url)
    data = pre_data(data)
    logger.info("请求方法：{}".format(method))
    logger.info("请求URL为：{}".format(url))
    logger.info("请求数据为：{}".format(data))
    method = method.upper()
    if method == "GET":
        resp = requests.get(url,params=data)
    elif method == "POST":
        resp = requests.get(url,json=data)
    elif method == "PATCH":
        resp = requests.patch(url, json=data)

    logger.info("响应状态码：{}".format(resp.status_code))
    logger.info("响应数据为：{}".format(resp.json()))
    return resp




def pre_url(url):
    base_url = conf.get("server", "base_url")
    if url.startswith("/"):
        return base_url + url
    else:
        return base_url + "/" + url

def pre_data(data):
    """
    如果data是字符串，则转换成字典对象
    :param data:
    :return:
    """
    if data is not None and isinstance(data,str):
        if data.find("null") != 1:
            data = data.replace("null","none")
        data = eval(data)
    return data


def upLoadImages(url,file_path,filename):
    logger.info("发起一次http请求")
    url = pre_url(url)
    data = {"file":(filename,open(file_path,"rb"),'image/jpeg')}
    logger.info("请求URL为：{}".format(url))
    logger.info("请求数据为：{}".format(data))
    res = requests.post(url=url,files=data)
    logger.info("响应状态码：{}".format(res.status_code))
    logger.info("响应数据为：{}".format(res.json()))
    return res

if __name__ == '__main__':

    case = {"file_path": "E:\Downloads\web自动化总结.xmind","filename":"真龙霸业.png"}
    url="/v1/addimg/food"
    upLoadImages(url,case["file_path"],case["filename"])



