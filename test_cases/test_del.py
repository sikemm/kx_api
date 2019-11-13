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
import json
#该模块是用来在所有用例执行完之后，删除新增的pos档案，店铺
file_name = file_path.api_case_path
sheet_name = 'Del'
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
    def test_del(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        #替换测试用例中的params的参数
        # posid = int(getattr(Reflex,'PosId'))
        # storeid = int(getattr(Reflex,'StoreId'))
        # params = eval(case['Params'])
        # if case['Params'].find('#PosId#') !=-1:
        #     params['Id'] = posid
        # elif case['Params'].find('#StoreId#') !=-1:
        #     params['Id'] = storeid
        params = eval(re_replace(case['Params']))
        # params = json.dumps(jdata)
        print(type(params))
        print(params)

        MyLog().info('---=正在执行{0}模块第{1}条测试用例:{2}----'.format(case['Module'],case['CaseId'],case['Title']))
        MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))
        resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'header'))
        print(type(resp))
        print(resp)
        print(resp.text)
        MyLog().info('ActualResult：{}'.format(resp.text))



        try:
            #----------待优化-------
            ActualResult={}
            ActualResult['success'] = resp.json()['success']
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



