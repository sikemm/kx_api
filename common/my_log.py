#__coding__:'utf-8'
#auther:ly
import logging
from kx_api.common import file_path
from kx_api.common.my_config import MyConfig
class MyLog:
    '''该类为日志类，用例日志书写 日志收集，日志输出'''
    def __init__(self):
        self.con = MyConfig()

    def my_log(self,level,msg):
        my_logger = logging.getLogger('mylog')
        my_logger.setLevel(self.con.get_string('log','logger_level'))

        # formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s]-[日志信息]:%(message)s')
        formatter = logging.Formatter(self.con.get_string('log','log_formatter'))
        stream_haddle = logging.StreamHandler()
        stream_haddle.setLevel(self.con.get_string('log','shaddle_level'))
        stream_haddle.setFormatter(formatter)

        file_haddle = logging.FileHandler(file_path.test_log_path,encoding='utf-8')
        file_haddle.setLevel(self.con.get_string('log','fhaddle_level'))
        file_haddle.setFormatter(formatter)

        my_logger.addHandler(stream_haddle)
        my_logger.addHandler(file_haddle)


        if level.upper() == 'DEBUG':
            my_logger.debug(msg)
        elif level.upper() == 'INFO':
            my_logger.info(msg)
        elif level.upper() == 'WARNING':
            my_logger.warning(msg)
        elif level.upper() == 'ERROR':
            my_logger.error(msg)
        else:
            my_logger.critical(msg)

        my_logger.removeHandler(file_haddle)
        my_logger.removeHandler(stream_haddle)

    def info(self,msg):
        self.my_log('INFO',msg)

    def debug(self,msg):
        self.my_log('DEBUG',msg)

    def error(self,msg):
        self.my_log('ERROR',msg)

if __name__ == '__main__':
    MyLog().my_log('info','报错了11111')
