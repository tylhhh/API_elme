import os, unittest
from jsonpath import jsonpath
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_log import logger
from Common.myddt import ddt, data
from Common.handle_requests import req
from Common.handle_data import clear_EnvData_atts,EnvData,replace_case_by_regular
from Common.handle_extract_data import extract_data

excel_path = os.path.join(datas_dir, "eleme_cases.xlsx")
get_excel = HandleExcel(excel_path, "添加餐馆")
cases = get_excel.read_all_datas()
get_excel.close_file()


@ddt
class TestAddRestaurants(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("***************************添加餐馆用例开始*****************************************")
        clear_EnvData_atts()


    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("***************************添加餐馆用例开始*****************************************")

    @data(*cases)
    def test_add_restaurants(self, case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        replace_case_by_regular(case)
        if "password" in eval(case["request_data"]).keys():  # 用password来判断要执行登录用例
            resp = req.send_requests(case["method"],case["url"], json=case["request_data"])
            cookies = resp.cookies
            setattr(EnvData,"cookies",cookies)  # 设置cookies为全局变量

        if "file_path" in eval(case["request_data"]).keys():  # 用file_path来判断执行上传图片用例
            files_data = req.upLoadImages(eval(case["request_data"])["file_path"], eval(case["request_data"])["filename"])
            resp = req.send_requests(case["method"],case["url"], files=files_data)
        if case["extract_data"]:
            extract_data(case["extract_data"],resp.json())
        if "image_path" in eval(case["request_data"]).keys():
            resp = req.send_requests(case["method"],case["url"],json=case["request_data"],cookies=EnvData.cookies)
        expected = eval(case["expected"])
        logger.info("用例的期望结果为：{}".format(expected))
        try:
            if 'sussess' in expected.keys():
                self.assertEqual(resp.json()["sussess"], expected["sussess"])
            else:
                self.assertEqual(resp.json()["status"], expected["status"])  # 用jsonpath提取is_map的值

        except AttributeError as e:
            logger.exception("断言失败！")
            raise e
