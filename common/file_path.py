#__coding__:'utf-8'
#auther:ly
'''该文件主要是用来获取项目中所需要的文件路径'''

import os
import datetime
# 获取当前文件工作路径
current_path = os.path.realpath(__file__)
# 获取测试用例路径
api_case_path = os.path.join(os.path.split(os.path.split(current_path)[0])[0],'test_cases','api_case.xlsx')

#获取测试报告地址
now = datetime.datetime.now()
curr = now.strftime('%Y%m%d-')
test_report_path = os.path.join(os.path.split(os.path.split(current_path)[0])[0],'test_result','test_report',curr+'test_report.html')

#日志存储的地址
test_log_path = os.path.join(os.path.split(os.path.split(current_path)[0])[0],'test_result','test_log',curr+'kx.log')

#配置文件的地址
config_path = os.path.join(os.path.split(os.path.split(current_path)[0])[0],'conf','config.conf')

if __name__ == '__main__':
    # print(config_path)
    print(current_path)
    # print(test_report_path)