#__coding__:'utf-8'
#auther:ly
import re
import datetime
import time

def bill_number():
    '''账单编号可结合反射来做，有待优化
    BillNumber ： 年月日+PosCode+终端维护一个5位编码'''
    a = 1
    l = '00001'
    bill = []
    while a < 4:
        curr_time = datetime.datetime.now()
        # t = curr_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        t = curr_time.strftime('%Y-%m-%d')
        p = '\d'
        res = re.findall(p, t)
        s = '01'
        for i in res:
            s += i

        a += 1
        bill.append(s+l)
        l = '0000'+str(int(l)+1)
        print(l)
        time.sleep(1)
    return bill
print(bill_number())