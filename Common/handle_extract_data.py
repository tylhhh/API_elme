import jsonpath
from Common.handle_data import EnvData


def extract_data(extrct_exprs,respose_dict):
    """
    根据jsonpath提取表达式，从响应结果当中，提取数据并设置为环境变量EnvData类的类属性，作为全局变量使用
    :param extrct_exprs: 从Excel当中读取出来的，提取表达式的字符串
    :param respose_dict: http请求之后的响应结果
    :return:
    """
    # 将提取表达式转换成字典
    extract_dict = eval(extrct_exprs)
    # 遍历字典，key作为全局变量名，value是jsonpath提取表达式
    for key,value in extract_dict.items():
        # 提取
        res = str(jsonpath.jsonpath(respose_dict,value)[0])
        # 设置环境变量
        setattr(EnvData,key,res)
        print(getattr(EnvData,key))
