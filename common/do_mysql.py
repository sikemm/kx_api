#__coding__:'utf-8'
#auther:ly
from mysql import connector
from kx_api.common.my_config import MyConfig
class DoMysql:
    '''该类主要是用来操作数据库'''

    def do_mysql(self,query,flag = 1):
        '''
        :param query: sql查询语句
        :return: fetchone 获取一条返回tuple类型数据，
        fetchall 返回list of tuple类型数据[(),()]
        '''
        #连接数据库
        db_config = MyConfig().get_other('DB', 'db_config')
        conn = connector.connect(**db_config)
        #获取游标
        curser = conn.cursor()
        #操作数据库
        curser.execute(query)
        curser.commit()
        if flag == 1:
            resp = curser.fetchone()
        else:
            resp = curser.fetchall()
        return resp

if __name__ == '__main__':
    # do_mysql = DoMysql()
    # query = 'select * from '
    # resp = do_mysql.do_mysql(query)
    # print(resp)
    m = None
    p = [{"Id":642201231061680128,"Sort":642201231061680128,"PId":0,"Code":"1","Name":"1","PyCode":"11"},{"Id":642201468501229568,"Sort":642201468501229568,"PId":642201231061680128,"Code":"2","Name":"2","PyCode":"2"},{"Id":642201494715629568,"Sort":642201494715629568,"PId":642201468501229568,"Code":"3","Name":"3","PyCode":"33"},{"Id":642201547769380864,"Sort":642201547769380864,"PId":0,"Code":"4","Name":"4","PyCode":"4"},{"Id":642201595760607232,"Sort":642201595760607232,"PId":0,"Code":"5","Name":"5","PyCode":"5"},{"Id":642201780058324992,"Sort":642201780058324992,"PId":642201231061680128,"Code":"22","Name":"22","PyCode":"22"},{"Id":642201840678600704,"Sort":642201840678600704,"PId":642201231061680128,"Code":"33","Name":"33","PyCode":"33"},{"Id":642201949231382528,"Sort":642201949231382528,"PId":642201468501229568,"Code":"45","Name":"45","PyCode":"4545"}]
    for i in p:
        if i['Id'] == 642201231061680128:
            print(i['Id'])
            m = i['PId']

    print(m)