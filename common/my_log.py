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
        my_logger = logging.getLogger('my_logger')
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
    # MyLog().my_log('info','报错了11111')
    logging.warning('3523425')
# 日志类
#1、使用的内置模块：logging，使用时需要导入，import logging
#2、日志里面有两个东西：日志收集器   日志输出渠道
# 如果未设置自己的日志收集器，调用系统默认的，源码默认的日志收集器，root logger   默认收集warning级别以上的信息，可以修改源码来改变默认的日志收集级别，并且添加控制台作为日志输出渠道
#If the logger has no handlers, call basicConfig() to add a console handler with a pre-defined format.
#logging.debug() -----debug()函数里面调用 root----root = RootLogger(WARNING)，rootlogger这个类，初始化函数里面有个参数level，就是默认的日志收集级别
# 2、设置自己的日志收集器，指定日志的输出渠道：控制台，还是文本
# 第一步，设置日志收集器，指定日志收集器名称，如果不填写名称，默认又是root logger   If no name is specified, return the root logger.
my_logger = logging.getLogger('my_log')
# 第二步：指定日志收集器的收集日志级别
my_logger.setLevel('INFO')
# 第三步：指定日志输出渠道，指定日志输出的级别， 设置日志输出的格式
my_haddle = logging.FileHandler('filename')  #输出到文本，指定文件路径，编码，模式默认为 a 追加写
my_haddle.setLevel('INFO')
formatter =logging.Formatter('[%(asctime)s]-[%(levelname)s]-[日志信息]:%(message)s')
my_haddle.setFormatter(formatter)
# 第四步：连接日志收集器和日志输出渠道，对接，说明日志收集的输出到哪个渠道，输出的日志级别信息，是取日志收集和日志输出级别的交集
my_logger.addHandler(my_haddle)
# 第五步：打印日志
# my_logger.debug() #debug(),info(),error()等
# 第六步：移除是移除日志输出渠道，如果不移除，有缓存，会导致日志重复输出，先添加的渠道ch，后添加渠道fh，移除先移除fh，再移除ch
my_logger.removeHandler(my_haddle)

