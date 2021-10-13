import os, unittest
from jsonpath import jsonpath
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_log import logger
from Common.myddt import ddt, data
from Common.handle_requests import req



excel_path = os.path.join(datas_dir, "eleme_cases.xlsx")
get_excel = HandleExcel(excel_path, "搜索地址")
cases = get_excel.read_all_datas()
get_excel.close_file()


@ddt
class TestSearchAddress(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("***************************搜索地址用例开始*****************************************")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("***************************搜索地址用例结束*****************************************")

    @data(*cases)
    def test_search_address(self,case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        resp = req.send_requests(case["method"], case["url"], params=case["request_data"])
        try:
            self.assertIn(eval(case["request_data"])["keyword"], jsonpath(resp.json(),'$..name')[0])  # 判断查询出来的名字是否包含搜索关键字
        except AssertionError as e:
            logger.exception("断言失败!")
            raise e
