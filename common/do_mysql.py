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
    do_mysql = DoMysql()
    query = 'select * from '
    resp = do_mysql.do_mysql(query)
    print(resp)