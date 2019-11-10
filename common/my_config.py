#__coding__:'utf-8'
#auther:ly
import configparser
from kx_api.common import file_path
class MyConfig:
    '''该类实现配置文件的读取'''
    def __init__(self):
        self.con = configparser.ConfigParser()

    def get_string(self, section, option):
        '''获取字符串类型的数据'''
        self.con.read(filenames=file_path.config_path, encoding='utf-8')
        resp = self.con.get(section, option)
        return resp

    def get_int(self,section,option):
        #获取整数类型的数据
        self.con.read(filenames=file_path.config_path,encoding='utf-8')
        #获取值
        resp = self.con.getint(section,option)
        return resp

    def get_boolean(self,section,option):
        '''获取布尔值类型的数据'''
        self.con.read(filenames=file_path.config_path, encoding='utf-8')
        resp = self.con.getboolean(section,option)
        return resp

    def get_float(self,section,option):
        '''获取浮点类型的数据'''
        self.con.read(filenames=file_path.config_path, encoding='utf-8')
        resp = self.con.getfloat(section,option)
        return resp

    def get_other(self,section,option):
        '''获取元组、字典、列表类型的数据'''
        self.con.read(filenames=file_path.config_path, encoding='utf-8')
        resp = self.con.get(section,option)
        return eval(resp)

if __name__ == '__main__':
    resp = MyConfig().get_string('log','log_name')
    print(resp)