import os
from configparser import ConfigParser
from Common.handle_path import conf_dir


class HandleConfig(ConfigParser):
    def __init__(self, file_path):
        super().__init__()
        self.read(file_path, encoding="utf-8")


# 配置文件路径
file_path = os.path.join(conf_dir, "conf.ini")
conf = HandleConfig(file_path)

