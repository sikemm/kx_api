#__coding__:'utf-8'
#auther:ly
import unittest
from ddt import ddt,data,unpack
from kx_api.common.do_excel import DoExcel
from kx_api.common import file_path
from kx_api.common.http_request import HttpRequest
from kx_api.common.my_log import MyLog
from kx_api.common.reflex import Reflex
from kx_api.common.re_replace import re_replace
from kx_api.test_cases import test_auth
#该模块是用来执行baseinfo的测试用例

file_name = file_path.api_case_path
sheet_name = 'BaseInfo'
test_data = DoExcel(file_name).read_data(sheet_name)

@ddt
class TestCases(unittest.TestCase):
    '''该类主要是用来写测试用例'''
    def setUp(self):
        '''每次用例开始执行前，创建一个读写excel的对象'''
        self.f = DoExcel(file_name)

    def tearDown(self):
        pass

    @data(*test_data)
    def test_baseInfo(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        # params = eval(case['Params'])
        #替换测试用例中的params的参数
        # params = eval(re_replace(case['Params']))
        # if case['Module'] =='Auth':
        #     params = re_replace(case['Params'])
        # else:
        #     params = eval(re_replace(case['Params']))
        params = eval(re_replace(case['Params']))
        MyLog().info('---=正在执行{0}模块第{1}条测试用例:{2}----'.format(case['Module'], case['CaseId'], case['Title']))
        MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))
        resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'header'))
        MyLog().info('ActualResult：{}'.format(resp.text))

        if resp.text.find('PosId') !=-1:
            setattr(Reflex, 'ClientPosBind', str(resp.json()['Result']['Id']))
            setattr(Reflex, 'StoreId', str(resp.json()['Result']['StoreId']))
            setattr(Reflex, 'PosId', str(resp.json()['Result']['PosId']))

        try:
            #----------使用什么来断言，还有待考虑参考yapi上的接口返回来做demo-------
            ActualResult={}
            ActualResult['Success'] = resp.json()['Success']
            self.assertEqual(eval(case['ExpectedResult']),ActualResult)
            test_result = 'pass'
        except AssertionError as e:
            test_result = 'failed'
            error_message = resp.json()['Error']['Message']
            MyLog().error('ERROR：{}'.format(error_message))
            # MyLog().error('用例执行失败：{}'.format(e))
            raise e
        finally:
            self.f.write_data(case['CaseId']+1,9,resp.text,sheet_name)
            self.f.write_data(case['CaseId']+1,10,test_result,sheet_name)


