#__coding__:'utf-8'
#auther:ly

import requests
class HttpRequest:
    '''该类主要是完成http的get和post请求，并返回一个消息实体，可通过text，json（）查看具体内容,cookies = cookies'''

    def http_request(self,method,url,params,header):

        if method.upper() == 'GET':
            try:
                resp = requests.get(url,params=params,headers = header)
            except Exception as e:
                resp = 'get请求出错了:{}'.format(e)
        elif method.upper() == 'POST':
            try:
                resp = requests.post(url,data=params.encode(),headers = header)
            except Exception as e:
                resp = 'post请求出错了:{}'.format(e)
        elif method.upper() =='PUT':
            try:
                resp = requests.put(url, data=params, headers=header)
            except Exception as e:
                resp = 'put请求出错了:{}'.format(e)

        elif method.upper() == 'DELETE':
            try:
                resp = requests.delete(url, data = params, headers=header)
            except Exception as e:
                resp = 'delete请求出错了:{}'.format(e)

        else:
            print('不支持此种类型请求')
            resp = None
        return resp

if __name__ == '__main__':
    import json
    h = HttpRequest()
    params = {
  "TenancyName": "default",
  "StoreCode": "CD",
  "PosCode": "1",
  "CommunicationPassword": "123456",
  "MachineMac": "1",
  "MachineName": "1",
  "Platform": 1
}
    params = json.dumps(params)
    header = {
        'Content-Type': 'application/json;',
    }
    resp = h.http_request('post','http://192.168.1.41:11001/api/services/app/Auth/Bind',params,)
    print(resp.text)
