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

#该模块是用来执行web端基础信息模块的接口   webBase表单的测试用例

file_name = file_path.api_case_path
sheet_name = 'webBase'
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
    def test_web_base(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        #替换测试用例中的params的参数
        # params = eval(re_replace(case['Params']))
        params = re_replace(case['Params'])
        print(params)
        MyLog().info('---=正在执行{0}模块第{1}条测试用例:{2}----'.format(case['Module'],case['CaseId'],case['Title']))
        MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))
        resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'wheader'))
        print(resp)
        print(type(resp))
        print(resp.text)
        MyLog().info('ActualResult：{}'.format(resp.text))
        #登录成功后，返回的body里面带有token信息，需要将token信息放在header里面一起请求
        if resp.text.find('accessToken') !=-1:
            header = getattr(Reflex, 'wheader')
            AccessToken = resp.json()['result']['accessToken']
            header['Authorization'] = 'Bearer '+ AccessToken
            setattr(Reflex, 'wheader', header)
        print(getattr(Reflex,'wheader'))
        #新增店铺成功后，经营类型为真，返回的值设置storeId的值
        if resp.text.find('businessType')!=-1:
            setattr(Reflex,'StoreId',resp.json()['result']['id'])
        elif resp.text.find('communicationPassword') !=-1:
            setattr(Reflex,'PosId',resp.json()['result']['id'])
        print(getattr(Reflex,'PosId'))
        # if resp.text.find('businessType')!=-1:
        #     setattr(Reflex,'storeId',resp.json()['result']['id'])
        # elif resp.text.find('productCategoryId')!=-1:
        #     setattr(Reflex,'prodoctId',resp.json()['result']['id'])
        # elif resp.text.find('pId')!=-1:
        #     setattr(Reflex, 'prodoctCategrayId', resp.json()['result']['id'])
        # elif resp.text.find('paymentWayType')!=-1:
        #     setattr(Reflex, 'payWayId', resp.json()['result']['id'])

        try:
            #----------使用什么来断言，还有待考虑-------
            ActualResult={}
            ActualResult['success'] = resp.json()['success']
            self.assertEqual(eval(case['ExpectedResult']),ActualResult)
            test_result = 'pass'
        except AssertionError as e:
            test_result = 'failed'
            error_message = resp.json()['error']['message']
            MyLog().error('ERROR：{}'.format(error_message))
            # MyLog().error('用例执行失败：{}'.format(e))
            raise e
        finally:
            self.f.write_data(case['CaseId']+1,9,resp.text,sheet_name)
            self.f.write_data(case['CaseId']+1,10,test_result,sheet_name)


