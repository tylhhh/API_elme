import re
from Common.handle_config import conf
from Common.handle_log import logger


class EnvData:
    """
    存储用例要使用到的数据
    """
    pass


def clear_EnvData_atts():
    values = dict(EnvData.__dict__.items())
    for key, value in values.items():
        if key.startswith("__"):
            pass
        else:
            delattr(EnvData, key)



def replace_by_regular(data):
    res = re.findall("#(.*?)#", data)
    if res:
        for item in res:
            try:
                value = conf.get("data", item)
            except:
                try:
                    value = getattr(EnvData, item)
                except AttributeError:
                    continue
            data = data.replace("#{}#".format(item), str(value))
    return data


def replace_case_by_regular(case):
    for key, value in case.items():
        if value is not None and isinstance(value, str):  # 确保是个字符串
            case[key] = replace_by_regular(value)
    logger.info("正则表达式替换完成之后的请求数据：\n{}".format(case))
    return case


def replace_data(case, mark, real_data):
    for key, value in case.items():
        if value is not None and isinstance(value, str):
            if value.find(mark) != -1:
                case[key] = value.replace(mark, real_data)
    return case


