#__coding__:'utf-8'
#auther:ly

import requests
class HttpRequest:
    '''该类主要是完成http的get和post请求，并返回一个消息实体，可通过text，json（）查看具体内容'''

    def http_request(self,method,url,params):

        if method.upper() == 'GET':
            try:
                resp = requests.get(url,params=params)
            except:
                resp = 'get请求出错了'
        elif method.upper() == 'POST':
            try:
                resp = requests.post(url,data=params)
            except:
                resp = 'post请求出错了'
        else:
            print('不支持此种类型请求')
            resp = None
        return resp

if __name__ == '__main__':
    h = HttpRequest()
    params = {"storeId":"277307870011392"}
    resp = h.http_request('get','http://192.168.1.56:8003/BaseInfo/GetDepartments',params)
    print(resp.text)