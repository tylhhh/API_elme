import os, unittest
from jsonpath import jsonpath
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_log import logger
from Common.myddt import ddt, data
from Common.handle_requests import req

excel_path = os.path.join(datas_dir, "eleme_cases.xlsx")
get_excel = HandleExcel(excel_path, "获取城市列表")
cases = get_excel.read_all_datas()
get_excel.close_file()




@ddt
class TestGetCityInfo(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("***************************获取城市列表用例开始*****************************************")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("***************************获取城市列表用例开始*****************************************")

    @data(*cases)
    def test_get_city_info(self, case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        resp = req.send_requests(case["method"], case["url"], params=case["request_data"])
        expected = eval(case["expected"])
        logger.info("用例的期望结果为：{}".format(expected))
        try:
            if 'message' in expected.keys():
                self.assertEqual(resp.json()["message"], expected["message"])
            else:
                self.assertEqual(jsonpath(resp.json(), '$..is_map')[0], expected["is_map"])  # 用jsonpath提取is_map的值
                self.assertIsNotNone(jsonpath(resp.json(), '$..pinyin'))  # 判断地区名是否为空

        except AttributeError as e:
            logger.exception("断言失败！")
            raise e
