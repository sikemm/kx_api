#__coding__:'utf-8'
#auther:ly

# 执行用例，出具测试报告
import unittest
from kx_api.common import file_path
import HTMLTestRunnerNew
from kx_api.test_cases.test_case import TestCases
#创建测试集
suite = unittest.TestSuite()
loader = unittest.TestLoader()
#添加测试用例到suite
suite.addTest(loader.loadTestsFromTestCase(TestCases))

with open(file_path.test_report_path,'w') as file:
    # runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
    #                                           verbosity=2,
    #                                           title='快消接口测试报告',
    #                                           description='基础信息，账单，绑定接口',
    #                                           tester='ly')
    runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=2)
    runner.run(suite)