#!/usr/bin.env python3
# coding=utf-8

import hmac
import hashlib
import base64
import os
import json
import requests
from time import gmtime, strftime, sleep

class zaoshuRequests(object):

    def __init__(self, api_key, api_secret):
        self._api_key = api_key
        self._api_secret = api_secret

    def get(self,url, params=None):
        # get请求
        return requests.get(url, params=params, headers=self.get_headers('GET',query=params))

    def post(self, url, params=None, body=None ):
        # post请求
        return requests.post(url, params=params, data=body, headers=self.get_headers('POST',query=params,body=body))

    def patch(self,url, params=None, body=None ):
        # patch请求
        return requests.patch(url, params=params, data=body, headers=self.get_headers('PATCH', query=params, body=body))

    def get_headers(self, method, query=None, body=None):
        """
        获得请求头信息
        :param method: 请求类型 GET, POST, PATCH
        :param query: 查询条件
        :param body: 内参
        :return: 返回带签名的请求头
        """
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Date': strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()),
            'Authorization': ''
        }

        authorization = self.sign(self._api_secret, method, headers['Content-Type'], headers['Date'], query=query, body=body)
        headers['Authorization'] = 'ZAOSHU {0}:{1}'.format(self._api_key, authorization)

        return headers

    def sign(self, secret, method, content_type, date, query=None, body=None):
        """
        生成签名
        :param secret: API Secret
        :param method: 请求类型 GET, POST, PATCH
        :param content_type: 指网页中定义网络文件类型和编码信息
        :param date: GMT时间
        :param query: 查询条件, 在地址栏部分
        :param body: 内容
        :return: 签名结果
        """
        values = [method, content_type, date, ]

        if query:
            values.extend('%s=%s' % (k, query[k]) for k in sorted(query.keys()))
        else:
            values.append("")

        if body:
            values.append(body)
        else:
            values.append("")
        base_string = "\n".join(values)

        digest = hmac.new(secret.encode("utf-8"), base_string.encode("utf-8"), hashlib.sha256).digest()
        return base64.b64encode(digest).decode("utf-8")

class zaoshuSdk(object):

    def __init__(self, api_key, api_secret, base_url='https://openapi.zaoshu.io/v2'):
        self._api_key = api_key
        self._api_secret = api_secret

        self._base_url = base_url
        self.request = zaoshuRequests(api_key, api_secret)
        self.instance = Instance(self._base_url, self.request)
        self.user = User(self._base_url, self.request)


class Instance(object):
    #造数实例
    def __init__(self, baseurl, request):

        self._request = request
        self._base_url = baseurl
        self.instance_list_url = self._base_url + "/instances"
        self.instance_url = self._base_url + "/instance/:instance_id"
        self.instance_schema_url = self._base_url + "/instance/:instance_id/schema"
        self.task_list_url = self._base_url + "/instance/:instance_id/tasks"
        self.task_url =  self._base_url + "/instance/:instance_id/task/:task_id"
        self.download_url = self._base_url + "/instance/:instance_id/task/:task_id/result/file"


    def list(self):
        """
        获取实例列表
        :return: requests.Response
        """
        return self._request.get(self.instance_list_url)

    def item(self,instance_id):
        """
        获取实例详情
        :param instance_id: 运行实例的id编号，可以从实例列表中获取
        :return: requests.Response
        """
        url = self.instance_url.replace(':instance_id',instance_id)
        return self._request.get(url)

    def schema(self,instance_id):
        """
        获取单个实例的数据格式
        :param instance_id:
        :return: requests.Response
        """
        url = self.instance_schema_url.replace(':instance_id', instance_id)
        return self._request.get(url)

    def taskList(self,instance_id):
        """
        获取某实例下的任务列表
        :param instance_id:
        :return: requests.Response
        """
        url = self.task_list_url.replace(':instance_id', instance_id)
        return self._request.get(url)

    def task(self,instance_id, task_id):
        """
        获取某实例下，单个任务详情
        :param instance_id:
        :param task_id:
        :return: requests.Response
        """
        url = self.task_url.replace(':instance_id', instance_id).replace(':task_id', task_id)
        return self._request.get(url)

    def downloadRunData(self,instance_id, task_id, file_type='csv', dirpath=None, filename=None):
        """
        下载运行结果
        :param instance_id:
        :param task_id:
        :param filetype:
        :param dirpath:
        :return:
        """
        params = {"contentType":file_type}
        url = self.download_url.replace(':instance_id', instance_id).replace(':task_id', task_id)

        #发生请求，获取下载文件
        response = self._request.get(url,params=params)

        # 当前执行路径
        self.dataPath = os.path.abspath(os.getcwd()).strip()
        self.dirpath = 'datafile'

        #获取文件名 和 后缀
        self.filename = response.headers['content-disposition']
        self.filename = '/'+str(self.filename.replace("attachment; filename*=UTF-8''",''))
        self.suffix = '.'+self.filename.split('.')[-1]
        self.filename = self.filename.replace(self.suffix,'')

        #配置保存路径
        if dirpath:
            #去除字符串后面的/
            if dirpath[-1] == '/':
                dirpath = dirpath[:-1]

            #判断路径是否存在

            if not dirpath[0] == '/':
                dirpath = '/'+dirpath
                self.dirpath = self.dataPath+dirpath
            else:
                self.dirpath = dirpath

        #判断路径是否存在
        if not os.path.isdir(self.dirpath):
            os.makedirs(self.dirpath)

        #对保存文件名进行操作
        if filename:
            # 去除字符串后面的/
            if not filename[0] == '/':
                filename = '/' + filename
            #判断文件是否存在
            if not os.path.isfile(self.dirpath+filename+self.suffix):
                self.filename = filename

        #保存文件
        with open(self.dirpath+self.filename+self.suffix,'wb') as file:
            file.write(response.content)

        return os.path.abspath(self.dirpath+self.filename+self.suffix)

    def run(self, instance_id, body=None):
        """
        运行实例
        :param instance_id: 运行实例的id编号，可以从实例列表中获取
        :return: requests.Response
        """
        if body is None:
           body = '{}'

        if not isinstance(body, str):
            body = json.dumps(body)

        url = self.instance_url.replace(':instance_id', instance_id)
        return self._request.post(url,body=body)

    def edit(self,instance_id, title=None, result_notify_uri=None):
        #进行三目运算 内容为空时 为‘’空字符串
        body = {
            'title': title,
            'result_notify_uri': result_notify_uri
        }
        body = json.dumps(body)
        url = self.instance_url.replace(':instance_id', instance_id)
        return self._request.patch(url, body=body)

class User(object):

    def __init__(self, instance_url, request):
        self._base_url = instance_url
        self._request = request
        self.account_url = self._base_url+'/user/account'
        self.wallet_url = self._base_url+'/user/wallet'

    def account(self):
        """
        获得用户帐号信息
        :return:
        """
        return self._request.get(self.account_url)

    def wallet(self):
        """
        获得用户钱包信息
        :return:
        """
        return self._request.get(self.wallet_url)


#测试代码 部分
if __name__=='__main__':

    zaoshu_url = 'https://openapi.zaoshu.io/v2'

    api_key = '你的api_key'

    api_secret = '你的api_secret'

    sdk = zaoshuSdk(api_key, api_secret, base_url=zaoshu_url)

    print('====[获取用户的信息]========================================')
    response = sdk.user.account()
    print("链接："+response.url)
    print("状态："+str(response.status_code))
    print("返回内容："+response.text)
    print("返回头信息：",end='')
    print(response.headers)

    print('\n')



    print('====[获取用户的爬虫实例]========================================')
    # 获取用户的爬虫实例
    response = sdk.instance.list()
    print("链接：" + response.url)
    print("状态：" + str(response.status_code))
    print("返回内容：" + response.text)
    print("返回头信息：", end='')
    print(response.headers)
    print('\n')


    response_json = response.json()

    #获取实例详情
    if len(response_json['data']) > 0:
        instance_id = response_json['data'][0]['id']
        response = sdk.instance.item(instance_id)
        print('====[获取实例详情]========================================')
        print("链接：" + response.url)
        print("状态：" + str(response.status_code))
        print("返回内容：" + response.text)
        print("返回头信息：", end='')
        print(response.headers)
        print('\n')

    else:
        print("没有实例无法继续，请创建实例后继续")
        os._exit()

    # 获取实例的数据格式
    if len(response_json['data']) > 0:
        instance_id = response_json['data'][0]['id']
        response = sdk.instance.schema(instance_id)
        print('====[获取实例的数据格式]========================================')
        print("链接：" + response.url)
        print("状态：" + str(response.status_code))
        print("返回内容：" + response.text)
        print("返回头信息：", end='')
        print(response.headers)
        print('\n')

    else:
        print("没有实例无法继续，请创建实例后继续")
        os._exit()

    # 编辑实例的数据
    if len(response_json['data']) > 0:
        instance_id = response_json['data'][0]['id']
        response = sdk.instance.edit(instance_id, title='测试修改实例数据')
        print('====[编辑实例的数据]========================================')
        print("链接：" + response.url)
        print("状态：" + str(response.status_code))
        print("返回内容：" + response.text)
        print("返回头信息：", end='')
        print(response.headers)
        print('\n')

    else:
        print("没有实例无法继续，请创建实例后继续")
        os._exit()

    #运行实例
    if len(response_json['data']) > 0:
        instance_id = response_json['data'][-1]['id']
        response = sdk.instance.run(instance_id)
        print('====[运行实例]========================================')
        print("链接：" + response.url)
        print("状态：" + str(response.status_code))
        print("返回内容：" + response.text)
        print("返回头信息：", end='')
        print(response.headers)
        print('\n')
        print('暂停10秒,等待实例运行完成')
        sleep(10)
    else:
        print("没有实例无法继续，请创建实例后继续")
        os._exit()

    # 获取实例下的任务列表
    if len(response_json['data']) > 0:
        instance_id = response_json['data'][-1]['id']
        response = sdk.instance.taskList(instance_id)
        print('====[获取实例任务列表]========================================')
        print("链接：" + response.url)
        print("状态：" + str(response.status_code))
        print("返回内容：" + response.text)
        print("返回头信息：", end='')
        print(response.headers)
        print('\n')

    else:
        print("没有实例无法继续，请创建实例后继续")
        os._exit()

    tasks = response.json()

    # 获取任务详情
    if len(response_json['data']) > 0 and len(tasks['data']) > 0:
        instance_id = response_json['data'][-1]['id']
        task_id = tasks['data'][-1]['id']
        response = sdk.instance.task(instance_id, task_id)
        print('====[获取任务详情]========================================')
        print("链接：" + response.url)
        print("状态：" + str(response.status_code))
        print("返回内容：" + response.text)
        print("返回头信息：", end='')
        print(response.headers)
        print('\n')

    else:
        print("没有实例无法继续，请创建实例后继续")
        os._exit()

    # 实例任务数据下载
    if len(response_json['data']) > 0 and len(tasks['data']) > 0:
        instance_id = response_json['data'][-1]['id']
        task_id = tasks['data'][-1]['id']
        response = sdk.instance.downloadRunData(instance_id, task_id ,file_type='json')
        print('====[实例任务数据下载]========================================')
        print(response)

    else:
        print("没有实例无法继续，请创建实例后继续")
        os._exit()
