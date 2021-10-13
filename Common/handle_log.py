"""
日志操作步骤：
1、创建一个日志收集器
2、给日志收集器设置日志级别
3、给日志收集器创建一个输出渠道
4、给渠道设置一个日志输出内容的格式
5、将日志格式绑定到渠道当中
6、将设置好的渠道添加到日志收集器上
"""
import logging,os
from Common.handle_path import logs_dir
from Common.handle_config import conf

class HandleLog:

    def __init__(self,name,path):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.stream_handle = logging.StreamHandler()
        self.file_handle = logging.FileHandler(path,encoding="utf-8")
        fmt = '%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(lineno)dline-日志信息: %(message)s'
        self.stream_handle.setFormatter(logging.Formatter(fmt))
        self.file_handle.setFormatter(logging.Formatter(fmt))
        self.logger.addHandler(self.stream_handle)
        self.logger.addHandler(self.file_handle)

    def get_logger(self):
        return self.logger

    def __del__(self):
        self.logger.removeHandler(self.stream_handle)
        self.logger.removeHandler(self.file_handle)
        self.stream_handle.close()
        self.file_handle.close()


if conf.getboolean("log","file_ok"):
    file_path = os.path.join(logs_dir,conf.get("log","file_name")) # 自定义日志文件名称
else:
    file_path = None

eleme_logger = HandleLog(conf.get("log","name"), file_path)
logger = eleme_logger.get_logger()







