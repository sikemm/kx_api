#__coding__:'utf-8'
#auther:ly

# 执行用例，出具测试报告
import sys
sys.path.append('./')   #jenkin集成的时候，可能需要加的系统路径
import unittest
from kx_api.common import file_path
import HTMLTestRunnerNew
from kx_api.test_cases import test_auth,test_checkout,test_del

#创建测试集
suite = unittest.TestSuite()
loader = unittest.TestLoader()
#使用加载模块的方式添加测试用例到suite
suite.addTest(loader.loadTestsFromModule(test_auth))
suite.addTest(loader.loadTestsFromModule(test_del))
# suite.addTest(loader.loadTestsFromModule(test_checkout))

with open(file_path.test_report_path,'wb') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                              verbosity=2,
                                              title=file_path.curr+'快消接口测试报告',
                                              description='基础信息，账单，绑定接口',
                                              )
    # runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=2)
    runner.run(suite)