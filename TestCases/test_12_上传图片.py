import os, unittest
from jsonpath import jsonpath
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_log import logger
from Common.myddt import ddt, data
from Common.handle_requests import req

excel_path = os.path.join(datas_dir, "eleme_cases.xlsx")
get_excel = HandleExcel(excel_path, "上传图片")
cases = get_excel.read_all_datas()
get_excel.close_file()


@ddt
class TestUploadPictures(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        logger.info("***************************上传图片用例开始*****************************************")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("***************************上传图片用例开始*****************************************")

    @data(*cases)
    def test_upload_pictures(self, case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        files_data = req.upLoadImages(eval(case["request_data"])["file_path"],eval(case["request_data"])["filename"])
        resp = req.send_requests(case["method"],case["url"], files=files_data)
        expected = eval(case["expected"])
        logger.info("用例的期望结果为：{}".format(expected))
        try:
            if 'message' in expected.keys():
                self.assertEqual(resp.json()["message"], expected["message"])
            else:
                self.assertEqual(resp.json()["status"], expected["status"])  # 用jsonpath提取is_map的值

        except AttributeError as e:
            logger.exception("断言失败！")
            raise e
