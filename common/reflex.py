#__coding__:'utf-8'
#auther:ly
from kx_api.common.my_config import MyConfig
from kx_api.common.do_excel import DoExcel
from kx_api.common import file_path
import random
import datetime
class Reflex:
    '''反射类,实现对动态参数值修改、赋值、删除的操作'''
    #wheader用来存取web端 登陆后返回的token信息
    wheader = {
        'Content-Type': 'application/json;charset=utf-8',
    }
    #header用来存取pos端登陆后token信息
    header = {
        'Content-Type': 'application/json;charset=utf-8',
    }
    #公司编号和租户id
    TenancyName = MyConfig().get_string('base','TenancyName')
    TenantId = MyConfig().get_string('base','TenantId')  #租户id，配置文件设置的定值

    # ========新增店铺，新增pos，绑定pos成功后，获取对应店铺id，pos id，pos绑定id========
    StoreId = None
    PosId = None
    ClientPosBindId = None

   #获取新增店铺，新增pos，绑定pos需要的参数值
    BStoreCode = MyConfig().get_string('Bind', 'BStoreCode') #店铺编码 新增传入
    BPosCode = MyConfig().get_string('Bind', 'BPosCode')     #新增pos编码
    storeName = MyConfig().get_string('Bind', 'storeName')   #新增店铺名称
    MachineMac = MyConfig().get_string('Bind', 'MachineMac')
    MachineName = MyConfig().get_string('Bind', 'MachineName')



    #版本号信息
    CurrentVersion = MyConfig().get_string('CurrentVersion','CurrentVersion')  #最新的版本号
    #===================会员模块所需参数===================
    #会员办卡,客户名称、编码、电话号码随机生成5位，也用于新增商品时的商品名称，商品code
    PersonName = str(chr(random.randint(0x4e00, 0x9fbf)))
    # PersonName = None
    PersonCode = str(random.randint(0x4e00, 0x9fbf))

    #pos端会员办卡时需要的办卡时间，会员卡类型，等级
    JoinTime = str(datetime.datetime.now())
    MemberCardTypeId = '1'
    MemberCardTypeLevelId = '1'

    #客户id，会员id
    MemberPersonId = None
    MemberUserId = None
    MemberPersonName = None
    MemberPayId = None

    #===========上传账单模块所需的参数=======
    #账单号：读取excel里面的订单号
    # BillNumber = DoExcel(file_path.api_case_path).read_tel('billNumber')
    BillNumber = None
    #源单单号
    OriginalBillNumber = None
    # OriginalBillNumber = str(int(BillNumber)-1)
    #退单单号
    # TbillNumber = str(int(BillNumber) + 1)
    #商品分类主键
    BaseProductCategoryId = None
    #获取商品id
    ProductId = None
    #商品规格主键,获取基础信息时赋值
    ProductStandardId = None

    #结账方式主键,人名币，会员卡，任我行
    RMBId = None
    MemberCardPayId = None
    GraspPayId = None

    #任我行支付成功后，返回的数据,商户号，支付通返回的单号
    BusinessId = None
    GraspBillNumberId = None

    # 用户登陆信息pos端登录时的用户名和密码
    UserId = None
    UserName = 'ly'
    Password = '123456'

    #创建商品所需要的条形码
    BarCode= chr(random.randint(0x4e00, 0x9fbf))
    #用户班次号excel维护，每次交班后加1
    ShiftKey = None


if __name__ == '__main__':

    print(type(Reflex.BillNumber))
    print(Reflex.BillNumber)
    print(Reflex.OriginalBillNumber)
    print(Reflex.TbillNumber)