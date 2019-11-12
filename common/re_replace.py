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

def findId(target,key,value):
    '''
    此方法主要是用来根据上一步骤的id，查找与之相关联的id
    :param target: 请求返回的结果
    :param key: 查看的字段
    :param value: 查找的字段的值
    :return: i ,找到了就直接返回整个字典
    '''
    for i in target:
        if i[key] == value:
            return i



if __name__ == '__main__':
    # p = '#(.*?)#'
    # target = '{"ClientPosBind":"#ClientPosBind#","StoreId":"#StoreId#","PosId":"#PosId#","MachineMac":"#MachineMac#","MachineName":"#MachineName#"}'
    # target1 = '{"id":"#storeId#","sort":"sort","tenantId":"sort","isActive":True,"code":"sort","name":"sort","pyCode":"sort","businessType":1,"businessTypeName":"直营","province":"四川省","city":"成都市","zone":"武侯区","street":"武侯大道888号","openTime":"08:00","closeTime":"22:00","address":"新希望大厦B座","storePhone":"15222222222","longitude":"经度","latitude":"纬度",}'
    # print(type(target1))
    # print(re_replace(target1))
    # print(re.search(p,target).group())
    p = [{"Id":642201231061680128,"Sort":642201231061680128,"PId":0,"Code":"1","Name":"1","PyCode":"11"},{"Id":642201468501229568,"Sort":642201468501229568,"PId":642201231061680128,"Code":"2","Name":"2","PyCode":"2"},{"Id":642201494715629568,"Sort":642201494715629568,"PId":642201468501229568,"Code":"3","Name":"3","PyCode":"33"},{"Id":642201547769380864,"Sort":642201547769380864,"PId":0,"Code":"4","Name":"4","PyCode":"4"},{"Id":642201595760607232,"Sort":642201595760607232,"PId":0,"Code":"5","Name":"5","PyCode":"5"},{"Id":642201780058324992,"Sort":642201780058324992,"PId":642201231061680128,"Code":"22","Name":"22","PyCode":"22"},{"Id":642201840678600704,"Sort":642201840678600704,"PId":642201231061680128,"Code":"33","Name":"33","PyCode":"33"},{"Id":642201949231382528,"Sort":642201949231382528,"PId":642201468501229568,"Code":"45","Name":"45","PyCode":"4545"}]
    print(findId(p,'Id',642201231061680128))
