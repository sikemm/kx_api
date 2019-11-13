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
import random
#该模块是用来执行Member表单的测试用例,新增会员，修改会员，停启用，会员支付等接口

file_name = file_path.api_case_path
sheet_name = 'BMember'
test_data = DoExcel(file_name).read_data(sheet_name)

print(test_data)
@ddt
class TestCases(unittest.TestCase):
    '''该类主要是用来写测试用例'''
    def setUp(self):
        '''每次用例开始执行前，创建一个读写excel的对象'''
        self.f = DoExcel(file_name)

    def tearDown(self):
        pass

    @data(*test_data)
    def test_bmember(self,case):
        global test_result
        method = case['Method']
        url = case['url']
        #替换测试用例中的params的参数
        if case['Params'] == None:
            params = case['Params']
        elif case['Method'].upper() =='POST':
            params = re_replace(case['Params'])
        elif case['Method'].upper() =='GET':
            params = eval(re_replace(case['Params']))
        print(params)
        MyLog().info('---=正在执行{0}模块第{1}条测试用例:{2}----'.format(case['Module'],case['CaseId'],case['Title']))
        MyLog().info('URL：{0}，Params：{1}'.format(case['url'],params))
        resp = HttpRequest().http_request(method, url, params,getattr(Reflex,'header'))
        MyLog().info('ActualResult：{}'.format(resp.text))

        print(resp.text)
        # 绑定成功后，获取服务器返回的店铺storeid等,posid,绑定posid，注意str的使用，设置时，只能是字符串
        if resp.text.find('businessType') != -1:
            setattr(Reflex, 'StoreId', resp.json()['result']['id'])
        elif resp.text.find('communicationPassword') != -1:
            setattr(Reflex, 'PosId', resp.json()['result']['id'])
        elif resp.text.find('PosId') != -1:
            setattr(Reflex, 'ClientPosBindId', str(resp.json()['Result']['Id']))

        # web登录成功后，返回的body里面带有token信息，需要将token信息放在header里面一起请求
        if resp.text.find('accessToken') != -1:
            header = getattr(Reflex, 'header')
            AccessToken = resp.json()['result']['accessToken']
            header['Authorization'] = 'Bearer ' + AccessToken
            setattr(Reflex, 'header', header)
        # pos端登陆成功之后，获取服务器返回的token信息
        elif resp.text.find('AccessToken') != -1:
            header = getattr(Reflex, 'header')
            AccessToken = resp.json()['Result']['AccessToken']
            header['Authorization'] = 'Bearer ' + AccessToken
            setattr(Reflex, 'header', header)
        #获取会员类型，会员卡等级[随便找一个，用于会员卡新增,现在是默认写死的
        # if url.find('GetMemberCardTypeLevelList') !=-1:
        #     setattr(Reflex, 'MemberCardTypeLevelId', str(resp.json()['Result'][0]['Id']))
        #     setattr(Reflex, 'MemberCardTypeId', str(resp.json()['Result'][0]['MemberCardTypeId']))
        #新增会员成功后，获取客户id，会员id
        if case['url'].find('CreateMemberInfo') !=-1:
            setattr(Reflex,'MemberPersonId',str(resp.json()['Result']['Id']))
            setattr(Reflex,'MemberUserId',str(resp.json()['Result']['MemberUser']['Id']))
            setattr(Reflex, 'MemberPersonName', str(resp.json()['Result']['PersonName']))
            # 新增会员后，操作会员电话号码加1写入表格，便于下次使用
            tel = str(int(case['Params']['PersonPhone']) + 1)
            self.f.write_data(2, 1, tel, 'PersonPhone')

        #会员支付成功后，获取支付id
        if case['url'].find('MemberPay') !=-1:
            setattr(Reflex, 'MemberPayId', str(resp.json()['Result']['MemberPayId']))
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



