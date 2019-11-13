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
        '''每次用例开始执行前，创建一个读写excel的对象，读取出上传账单所需要的账单，班次号信息'''
        self.f = DoExcel(file_name)
        #获取账单编号，源单号
        BillNumber = self.f.read_tel('billNumber')
        OriginalBillNumber = str(int(BillNumber) - 1)
        setattr(Reflex,'BillNumber',BillNumber)
        setattr(Reflex, 'OriginalBillNumber', OriginalBillNumber)
        #获取班次号
        ShiftKey = self.f.read_tel('ShiftKey')
        setattr(Reflex,'ShiftKey',ShiftKey)
        #获取商品条码
        BarCode = self.f.read_tel('BarCode')
        setattr(Reflex, 'BarCode', BarCode)


    def tearDown(self):
        billnumber = str(int(getattr(Reflex, 'BillNumber')) + 1)
        self.f.write_data(2, 1, billnumber, 'billNumber')

    @data(*test_data)
    def test_checkOut(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        print(case['Params'])
        #替换测试用例中的params的参数
        if case['Params'] == None:
            params = case['Params']
        elif case['Method'].upper() == 'GET':
            params = eval(re_replace(case['Params']))
        elif case['Method'].upper() == 'DELETE':
            params = eval(re_replace(case['Params']))
        elif case['Method'].upper() == 'POST':
            params = re_replace(case['Params'])

        MyLog().info('---=正在执行{0}模块第{1}条测试用例:{2}----'.format(case['Module'],case['CaseId'],case['Title']))
        MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))
        #发起请求
        resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'header'))
        print(type(resp))
        print(resp)
        print(resp.text)
        MyLog().info('ActualResult：{}'.format(resp.text))

        # 会员支付成功后，获取支付id
        if case['url'].find('MemberPay') != -1:
            setattr(Reflex, 'MemberPayId', str(resp.json()['Result']['MemberPayId']))

        #交班之后，重新登陆，重新获取token
        if resp.text.find('AccessToken') != -1:
            header = getattr(Reflex, 'header')
            AccessToken = resp.json()['Result']['AccessToken']
            header['Authorization'] = 'Bearer ' + AccessToken
            setattr(Reflex, 'header', header)

        #执行了交班，表格里面的班次号+1
        if url.find('PostShift') !=-1:
            ShiftKeyNew = str(int(getattr(Reflex,'ShiftKey'))+1)
            self.f.write_data(2,1,ShiftKeyNew,'ShiftKey')

        #执行了创建商品后，商品条码+1
        if url.find('CreateBaseProduct') !=-1:
            BarCodeNew = str(int(getattr(Reflex,'BarCode'))+1)
            self.f.write_data(2,1,BarCodeNew,'BarCode')

        try:
            #----------待优化-------
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



