#!/usr/bin.env python3
# coding=utf-8

"""
zaoshu 模块集成 ZaoshuRequests, ZaoshuSdk, Instance, User 类。
主要为造数api提供 接口服务
"""
import hmac
import hashlib
import base64
import os
import json
from io import BytesIO
from time import gmtime, strftime
import zipfile
import requests

__version__ = '0.2.0'

class ZaoshuRequests(object):
    """
       造数HTTP类，为每个请求附加符合造数规则的签名
       """

    def __init__(self, api_key, api_secret):
        """
        构造函数
        :param api_key: 从造数获取的api key
        :param api_secret:从造数获取的api secret
        """
        self._api_key = api_key
        self._api_secret = api_secret

    def get(self, url, params=None):
        """
        get请求
        :param url: 请求url
        :param params: 请求参数
        :return:requests.request
        """
        return requests.get(url, params=params, headers=self.get_headers('GET', query=params))

    def post(self, url, params=None, body=None):
        """
        post请求
        :param url:请求url
        :param params:请求参数
        :param body:内容
        :return:requests.request
        """
        return requests.post(url, params=params, data=body,
                             headers=self.get_headers('POST', query=params, body=body))

    def patch(self, url, params=None, body=None):
        """
        patch请求
        :param url:请求url
        :param params:请求参数
        :param body:内容
        :return:requests.request
        """
        return requests.patch(url, params=params, data=body,
                              headers=self.get_headers('PATCH', query=params, body=body))

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

        parame = {
            'query':query,
            'body':body
        }

        authorization = self.sign(self._api_secret, method, headers=headers, parame=parame)
        headers['Authorization'] = 'ZAOSHU {0}:{1}'.format(self._api_key, authorization)

        return headers

    @classmethod
    def sign(cls, secret, methods, headers=None, parame=None):
        """
        生成签名
        :param secret: API Secret
        :param methods: 请求类型 GET, POST, PATCH
        :param headers: 请求头信息包括 Content-Type, Date
        :param parame: 参数包括 查询条件query url参数 和 请求内容body
        :return: str 返回生成的sign签名结果
        """

        values = [methods, headers['Content-Type'], headers['Date'], ]

        if parame['query']:
            values.extend('%s=%s' % (k, parame['query'][k]) for k in sorted(parame['query'].keys()))
        else:
            values.append("")

        if parame['body']:
            values.append(parame['body'])
        else:
            values.append("")
            
        base_string = u"\n".join(values)

        digest = hmac.new(secret.encode("utf-8"), base_string.encode("utf-8"),
                          hashlib.sha256).digest()
        return base64.b64encode(digest).decode("utf-8")

class ZaoshuSdk(object):
    """
    造数SDK 这里整合里造数各功能类
    """

    def __init__(self, api_key, api_secret, base_url='https://openapi.zaoshu.io/v2'):
        self._api_key = api_key
        self._api_secret = api_secret

        self._base_url = base_url
        self.request = ZaoshuRequests(api_key, api_secret)
        self.instance = Instance(self._base_url, self.request)
        self.user = User(self._base_url, self.request)

    def get_api_key(self):
        """
        get api_key
        :return:
        """
        return self._api_key

    def get_api_secret(self):
        """
        get api_secret
        :return:
        """
        return self._api_secret

    def get_base_url(self):
        """
        get api_base_url
        :return:
        """
        return self._base_url

class Instance(object):
    """
    爬虫实例
    """
    def __init__(self, base_url, request):
        """
        构造函数
        :param base_url: 造数基本API接口
        :param request: 造数HTTP对象
        """
        self._request = request
        self.instance_list_url = base_url + "/instances"
        self.instance_url = base_url + "/instance/:instance_id"
        self.instance_schema_url = base_url + "/instance/:instance_id/schema"
        self.task_list_url = base_url + "/instance/:instance_id/tasks"
        self.task_url = base_url + "/instance/:instance_id/task/:task_id"
        self.download_url = base_url + "/instance/:instance_id/task/:task_id/result/file"

    def list(self):
        """
        获取实例列表
        :return: requests.Response
        """
        return self._request.get(self.instance_list_url)

    def item(self, instance_id):
        """
        获取实例详情
        :param instance_id: 运行实例的id编号，可以从实例列表中获取
        :return: requests.Response
        """
        url = self.instance_url.replace(':instance_id', instance_id)
        return self._request.get(url)

    def schema(self, instance_id):
        """
        获取单个实例的数据格式
        :param instance_id:
        :return: requests.Response
        """
        url = self.instance_schema_url.replace(':instance_id', instance_id)
        return self._request.get(url)

    def task_list(self, instance_id):
        """
        获取某实例下的任务列表
        :param instance_id:
        :return: requests.Response
        """
        url = self.task_list_url.replace(':instance_id', instance_id)
        return self._request.get(url)

    def task(self, instance_id, task_id):
        """
        获取某实例下，单个任务详情
        :param instance_id:
        :param task_id:
        :return: requests.Response
        """
        url = self.task_url.replace(':instance_id', instance_id).replace(':task_id', task_id)
        return self._request.get(url)

    def download_run_data(self, instance_id, task_id, file_type='csv', save_file=False, save_path = None):
        """
        下载运行结果
        :param instance_id: 实例ID
        :param task_id: 任务ID
        :param file_type: 文件类型
        :param save_file:
        :return:保存文件的路径/StringIO对象
        """
        params = {"contentType":file_type}
        url = self.download_url.replace(':instance_id', instance_id).replace(':task_id', task_id)

        # 发生请求，获取下载文件
        response = self._request.get(url, params=params)

        default_file_name = response.headers['content-disposition']
        default_file_name = '/' + str(default_file_name.replace("attachment; filename*=UTF-8''",
                                                                ''))
        suffix = '.' + default_file_name.split('.')[-1]
        default_file_name = default_file_name.replace(suffix, '')

        #判断是否保存文件
        if save_file and save_path:

            default_dir_path = '.'+save_path+'/datafile'
            # 获取文件名 和 后缀

            # 这里需要对权限进行配置，暂后做
            # 判断路径状态
            if not os.path.isdir(default_dir_path):
                os.makedirs(default_dir_path)

            # 保存文件
            save_file_path = default_dir_path+default_file_name+suffix

            with open(save_file_path, 'wb') as file:
                file.write(response.content)
            return os.path.abspath(save_file_path)
        elif save_file:
            raise Exception("save_path Error")
        else:
            download_file = BytesIO(response.content)
            if suffix in '.zip':
                surface = ''
                depth = ''
                decom_bytes = zipfile.ZipFile(file=download_file)
                # 获取文件名
                if len(decom_bytes.namelist()) == 2:
                    surface = decom_bytes.read(decom_bytes.namelist()[0])
                    depth = decom_bytes.read(decom_bytes.namelist()[-1])

                return surface.decode(), depth.decode()
            else:
                return response.content.decode(),


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
        return self._request.post(url, body=body)

    def edit(self, instance_id, title=None, result_notify_uri=None):
        """
        实例编辑
        :param instance_id: 实例id
        :param title: 要修改的实例标题
        :param result_notify_uri: 回调url
        :return:
        """
        body = {
            'title': title,
            'result_notify_uri': result_notify_uri
        }
        body = json.dumps(body)
        url = self.instance_url.replace(':instance_id', instance_id)
        return self._request.patch(url, body=body)

class User(object):
    """
    用户类
    """

    def __init__(self, base_url, request):
        """
        构造函数
        :param base_url: 造数基础API 接口
        :param request: 造数HTTP类
        """
        self._base_url = base_url
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
