#__coding__:'utf-8'
#auther:ly
import re
from kx_api.common.reflex import Reflex
def  re_replace(target):
    '''
    该函数主要是使用正则完成测试用例中params参数的替换
    re.search当找到和p规则匹配的数据就返回，返回一个对象，true
    m.group()等同于group(0)函数,返回的是匹配的整个字符串#括号里面的#
    m.group(1)返回的是匹配的第一个括号里面的字符串'''
    p='#(.*?)#'
    while re.search(p,target):
        m=re.search(p,target)
        key = getattr(Reflex,m.group(1))
        #每替换一次就将最新的字符串赋值给taget
        target =re.sub(p,key,target,count=1)
    return target


if __name__ == '__main__':
    p = '#(.*?)#'
    target = '{"ClientPosBind":"#ClientPosBind#","StoreId":"#StoreId#","PosId":"#PosId#","MachineMac":"#MachineMac#","MachineName":"#MachineName#"}'
    target1 = '{"id":"#storeId#","sort":"sort","tenantId":"sort","isActive":True,"code":"sort","name":"sort","pyCode":"sort","businessType":1,"businessTypeName":"直营","province":"四川省","city":"成都市","zone":"武侯区","street":"武侯大道888号","openTime":"08:00","closeTime":"22:00","address":"新希望大厦B座","storePhone":"15222222222","longitude":"经度","latitude":"纬度",}'
    print(type(target1))
    print(re_replace(target1))
    # print(re.search(p,target).group())
