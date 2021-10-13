import os, unittest
from jsonpath import jsonpath
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_log import logger
from Common.myddt import ddt, data
from Common.handle_requests import req
from Common.handle_data import replace_case_by_regular
from Common.handle_extract_data import extract_data

excel_path = os.path.join(datas_dir, "eleme_cases.xlsx")
get_excel = HandleExcel(excel_path, "获取商铺列表")
cases = get_excel.read_all_datas()
get_excel.close_file()


@ddt
class TestGetRestaurantsList(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("***************************获取商铺列表用例开始*****************************************")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("***************************获取商铺列表用例结束*****************************************")

    @data(*cases)
    def test_get_restaurants_list(self, case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        replace_case_by_regular(case)
        resp = req.send_requests(case["method"], case["url"], params=case["request_data"])
        if case["extract_data"]:
            extract_data(case["extract_data"],resp.json())
        if case["expected"]:
            expected = eval(case["expected"])
            logger.info("期望结果：{}".format(expected))
            try:
                if 'message' in expected.keys():
                    self.assertEqual(resp.json()["message"], expected["message"])
                else:
                    print(jsonpath(resp.json(), '$..id'))
                    self.assertIsNotNone(jsonpath(resp.json(), '$..id'))  # 判断商铺列表是否为空
            except AssertionError as e:
                logger.exception("断言失败!")
                raise e

