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

#该模块是用来执行checkout表单的测试用例，主要是操作账单数据

file_name = file_path.api_case_path
sheet_name = 'CheckOut'
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
    def test_checkOut(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        #替换测试用例中的params的参数
        params = re_replace(case['Params'])
        MyLog().info('---=正在执行{0}模块第{1}条测试用例:{2}----'.format(case['Module'],case['CaseId'],case['Title']))
        MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))
        resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'header'))
        print(resp.text)
        MyLog().info('ActualResult：{}'.format(resp.text))
        # 绑定成功后，获取服务器返回的绑定posid，店铺storeid等,注意str的使用，设置时，只能是字符串
        if resp.text.find('PosId') != -1:
            setattr(Reflex, 'ClientPosBind', str(resp.json()['Result']['Id']))
            setattr(Reflex, 'StoreId', str(resp.json()['Result']['StoreId']))
            setattr(Reflex, 'PosId', str(resp.json()['Result']['PosId']))
        # 登陆成功之后，获取服务器返回的token信息
        if resp.text.find('AccessToken') != -1:
            header = getattr(Reflex, 'header')
            AccessToken = resp.json()['Result']['AccessToken']
            header['Authorization'] = 'Bearer ' + AccessToken
            # 用户登录时，会返回一个班次号信息
            # ShiftKey = resp.json()['Result']['ShiftKey']
            # setattr(Reflex,'ShiftKey',ShiftKey)
            setattr(Reflex, 'header', header)
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
            MyLog().error('用例执行失败：{}'.format(e))
            raise e
        finally:
            self.f.write_data(case['CaseId']+1,9,resp.text,sheet_name)
            self.f.write_data(case['CaseId']+1,10,test_result,sheet_name)


