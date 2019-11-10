#__coding__:'utf-8'
#auther:ly
import unittest
from ddt import ddt,data,unpack
from kx_api.common.do_excel import DoExcel
from kx_api.common import file_path
from kx_api.common.http_request import HttpRequest
from kx_api.common.my_log import MyLog


file_name = file_path.api_case_path
sheet_name = 'BaseInfo'
test_data = DoExcel(file_name, sheet_name).read_data()

@ddt
class TestCases(unittest.TestCase):
    '''该类主要是用来写测试用例'''
    def setUp(self):
        '''每次用例开始执行前，创建一个读写excel的对象'''
        self.f = DoExcel(file_name, sheet_name)

    def tearDown(self):
        pass

    @data(*test_data)
    def test_case(self,case):
        method = case['Method']
        url = case['url']
        params = eval(case['Params'])
        MyLog().info('正在执行第{}条测试用例'.format(case['CaseId']))
        MyLog().info('测试的数据是：{}'.format(case))
        resp = HttpRequest().http_request(method, url, params)
        try:
            self.assertEqual(eval(case['ExpectedResult']),resp.json())
            test_result = 'pass'
        except AssertionError as e:
            test_result = 'failed'
            MyLog().error('用例执行失败了：{}'.format(e))
            raise e

        finally:
            self.f.write_data(case['CaseId']+1,8,resp.text)
            self.f.write_data(case['CaseId']+1,9,test_result)
        MyLog().info('实际结果是：{}'.format(resp.text))


#单元测试，主要是用于对某个类，模块进行测试，一般是开发做的，使用框架：unittest
#测试：使用单元测试框架+ddt 来进行自动化测试
#unittest   1、测试用例----使用类TestCase （TestCase的一个实例就是一个测试用例），测试用例要使用test_开头，才会被识别为一条测试用例
# 用例执行的顺序，是按照ascii编码来执行的，比如两个测试用例：test_add_dec   test_add_edc   前面的字母一样，d/e不同，
# ascii编码里面，d在e前面，所以先执行test_add_dec这条用例
# 2、执行用例   类TestSuite 来装测试用例    类TestTextRunner  执行测试
# 3、出具测试报告 类TestTextRunner
