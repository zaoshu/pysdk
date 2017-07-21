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
from time import gmtime, strftime, sleep

import requests

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

    def sign(self, secret, methods, headers=None, parame=None):
        """
        生成签名
        :param secret: API Secret
        :param methods: 请求类型 GET, POST, PATCH
        :param headers: 设置
        :param date: GMT时间
        :param query: 查询条件, 在地址栏部分
        :param body: 内容
        :return: 签名结果
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
        base_string = "\n".join(values)

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

    def download_run_data(self, instance_id, task_id, file_type='csv', dir_path=None,
                          file_name=None):
        """
        下载运行结果
        :param instance_id: 实例ID
        :param task_id: 任务ID
        :param file_type: 文件类型
        :param dir_path: 保存路径
        :param file_name: 文件名字
        :return: 保存文件的路径
        """
        params = {"contentType":file_type}
        url = self.download_url.replace(':instance_id', instance_id).replace(':task_id', task_id)

        # 发生请求，获取下载文件
        response = self._request.get(url, params=params)

        # 当前执行路径
        # run_path = os.path.abspath(os.getcwd()).strip()
        default_dir_path = 'datafile'

        # 获取文件名 和 后缀
        default_file_name = response.headers['content-disposition']
        default_file_name = '/'+str(default_file_name.replace("attachment; filename*=UTF-8''", ''))
        suffix = '.'+default_file_name.split('.')[-1]
        default_file_name = default_file_name.replace(suffix, '')

        # 配置保存路径
        if dir_path:
            # 去除字符串后面的/
            if dir_path[-1] == '/':
                dir_path = dir_path[:-1]

            # 判断是路径还是文件夹
            if not dir_path[0] == '/':
                default_dir_path = default_dir_path+'/'+dir_path
            else:
                default_dir_path = dir_path

        # 判断路径状态
        if not os.path.isdir(default_dir_path):
            os.makedirs(default_dir_path)

        # 对保存文件名进行操作
        if file_name:
            # 去除字符串后面的/
            if not file_name[0] == '/':
                file_name = '/' + file_name
            # 判断文件是否存在
            if not os.path.isfile(default_dir_path+file_name+suffix):
                default_file_name = file_name

        # 保存文件
        save_file_path = default_dir_path+default_file_name+suffix

        with open(save_file_path, 'wb') as file:
            file.write(response.content)

        return os.path.abspath(save_file_path)

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

def print_resopnse_info(response, title=''):
    """
    输出响应信息
    :param response:response响应对象
    :param title: 显示标题
    :return: None
    """
    print('====[%s]========================================'% title)
    print("链接："+response.url)
    print("状态："+str(response.status_code))
    print("返回内容："+response.text)
    print("返回头信息：", end='')
    print(response.headers)
    print('\n')

# 测试代码 部分
if __name__ == '__main__':

    ZAOSHU_URL = 'https://openapi.zaoshu.io/v2'

    # api_key = '你的api_key'
    API_KEY = 'ca3a56bdb5594c2b9e6d3f87f3d35baf'

    # api_secret = '你的api_secret'
    API_SERVER = '80518755f8d5d91f730a9332e2941023e41e29a856e6285bf51901af2f50f2b0'

    sdk = ZaoshuSdk(API_KEY, API_SERVER, base_url=ZAOSHU_URL)

    # 获取用户账户信息
    user_account_response = sdk.user.account()
    print_resopnse_info(user_account_response, '获取用户账户信息')

    # 获取用户钱包信息
    user_wallet_response = sdk.user.wallet()
    print_resopnse_info(user_wallet_response, '获取用户钱包信息')

    # 获取用户的爬虫实例
    instance_list_response = sdk.instance.list()
    print_resopnse_info(instance_list_response, '获取用户的爬虫实例')


    response_json = instance_list_response.json()

    # 获取实例详情
    if response_json['data']:
        # 实例id
        instance_id = response_json['data'][0]['id']

        # 获取实例详情
        instance_item_response = sdk.instance.item(instance_id)
        print_resopnse_info(instance_item_response, '获取实例详情')

        # 获取实例的数据格式
        instance_schema_response = sdk.instance.schema(instance_id)
        print_resopnse_info(instance_schema_response, '获取实例的数据格式')

        # 编辑实例的数据
        instance_edit_response = sdk.instance.edit(instance_id, title='测试修改实例数据标题')
        print_resopnse_info(instance_edit_response, '编辑实例的数据')

        # 运行实例
        instance_run_response = sdk.instance.run(instance_id)
        print_resopnse_info(instance_run_response, '运行实例')
        print('暂停10秒,等待实例运行完成')
        sleep(10)

        # 获取实例任务列表
        instance_task_list_response = sdk.instance.task_list(instance_id)
        print_resopnse_info(instance_task_list_response, '获取实例任务列表')

        # 解析实例任务列表
        tasks = instance_task_list_response.json()

        # 获取任务详情
        if tasks['data']:
            # 任务id
            task_id = tasks['data'][-1]['id']

            # 获取任务详情
            instance_task_response = sdk.instance.task(instance_id, task_id)
            print_resopnse_info(instance_task_response, '获取任务详情')

            # 实例任务数据下载
            instance_download_path = sdk.instance.download_run_data(instance_id, task_id,
                                                                    file_type='json')
            print('====[实例任务数据下载]========================================')
            print('下载路径：'+instance_download_path)

    else:
        print("没有实例无法继续，请创建实例后继续")
