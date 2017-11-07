#!/usr/bin.env python3
# coding=utf-8

"""
造数模块的单元测试
"""
import unittest

import requests
from zaoshu import Instance
from zaoshu import User
from zaoshu import ZaoshuRequests
from zaoshu import ZaoshuSdk
from io import BytesIO
import os

# 使用测试key
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
INSTANCE_ID = os.environ.get('INSTANCE_ID')
TASK_ID = os.environ.get('TASK_ID')

# API_KEY = '775673cc0b90406cb60d4bd3c87ac017'
# API_SECRET = '6b89554d1abd52b16e695ae773bc01ee69e68f720b4136aed05f4ad28db02910'
# INSTANCE_ID = '9369e046a59f40ad90ccc29ca943476d'
# TASK_ID = '51c528e0570d4f1ab3011893b8887535'

class TestZaoshuRequests(unittest.TestCase):
    """
    造数Http库ZaoshuRequests单元测试
    """
    def setUp(self):
        """初始化工作"""
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.request = ZaoshuRequests(self.api_key, self.api_secret)

    def test_sign(self):
        """测试签名"""
        query = {
            'a': '1',
            'b': '2',
        }
        body = '{"v":"tt"}'
        methods = 'POST'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Date': 'Wed, 18 Mar 2016 08:04:06 GMT'
        }
        parame = {
            'query': query,
            'body': body
        }
        api_secret = '1234567890-='

        sign = self.request.sign(api_secret, methods=methods, headers=headers, parame=parame)
        self.assertEqual(sign, 'QzXPkAH7JU5CtFRilL0GgRgdxYyqXKnwdln94ZARis0=')

    def test_get_headers(self):
        """测试获取请求头信息"""
        query = {
            'a': '1',
            'b': '2',
        }

        body = '{"v":"tt"}'
        methods = 'POST'

        headers = self.request.get_headers(method=methods, query=query, body=body)
        self.assertNotEqual(headers['Authorization'], '')
        self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')

    def test_get(self):
        """测试get请求"""
        base_url = 'https://openapi.zaoshu.io/v2'

        get_request = self.request.get(base_url)
        self.assertTrue(isinstance(get_request, requests.models.Response))


class TestZaoshuSdk(unittest.TestCase):
    """
    造数SDK ZaoshuSdk 单元测试
    """

    def setUp(self):
        """初始化工作"""
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.sdk = ZaoshuSdk(self.api_key, self.api_secret)

    def test(self):
        """测试造数SDK"""
        sdk = ZaoshuSdk(self.api_key, self.api_secret)

        self.assertTrue(isinstance(sdk.request, ZaoshuRequests))
        self.assertTrue(isinstance(sdk.instance, Instance))
        self.assertTrue(isinstance(sdk.user, User))

class TestInstance(unittest.TestCase):
    """
    造数 实例 Instance 单元测试
    """

    def setUp(self):
        """初始化工作"""
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.request = ZaoshuRequests(self.api_key, self.api_secret)
        self.base_url = 'https://openapi.zaoshu.io/v2'
        self.instance = Instance(self.base_url, self.request)
        self.instance_id = INSTANCE_ID
        self.task_id = TASK_ID

    def test_1_list(self):
        """测试获取用户的爬虫实例列表"""
        instance_list_response = self.instance.list()
        self.assertEqual(instance_list_response.status_code, 200)
        self.instance_id = instance_list_response.json()['data'][0]['id']

    def test_2_item(self):
        """测试获取单个爬虫实例实例"""
        self.assertNotEqual(self.instance_id, '')
        instance_item_response = self.instance.item(self.instance_id)
        self.assertEqual(instance_item_response.status_code, 200)

    def test_3_schema(self):
        """测试获取实例数据结构"""
        instance_schema_response = self.instance.schema(self.instance_id)
        self.assertEqual(instance_schema_response.status_code, 200)

    def test_4_edit(self):
        """测试编辑实例"""
        instance_edit_response = self.instance.edit(self.instance_id,
                                                    title='测试修改实例数据标题')
        self.assertEqual(instance_edit_response.status_code, 200)

    def test_5_run(self):
        """测试运行实例"""
        instance_run_response = self.instance.run(self.instance_id)
        self.assertEqual(instance_run_response.status_code, 200)

    def test_6_task_list(self):
        """测试获取实例任务列表"""
        instance_task_list_response = self.instance.task_list(self.instance_id)
        self.assertEqual(instance_task_list_response.status_code, 200)
        self.task_id = instance_task_list_response.json()['data'][-1]['id']

    def test_7_task(self):
        """测试获取实例任务详情"""
        instance_task_response = self.instance.task(self.instance_id, self.task_id)
        self.assertEqual(instance_task_response.status_code, 200)

    def test_8_download_run_data(self):
        """测试下载运行结果数据"""

        instance_download_path = self.instance.download_run_data(self.instance_id,
                                                                 self.task_id,
                                                                 file_type='json',
                                                                 save_file='test1',save_path="/date")
        instance_download_count = self.instance.download_run_data(self.instance_id,
                                                                 self.task_id,
                                                                 file_type='json')

        self.assertNotEqual(instance_download_path, "")
        self.assertTrue(isinstance(instance_download_count, BytesIO))


class TestUser(unittest.TestCase):
    """测试用户类"""

    def setUp(self):
        """初始化工作"""
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.request = ZaoshuRequests(self.api_key, self.api_secret)
        self.base_url = 'https://openapi.zaoshu.io/v2'
        self.user = User(self.base_url, self.request)

    def test_account(self):
        """测试账户信息"""
        user_account_response = self.user.account()
        self.assertEqual(user_account_response.status_code, 200)

    def test_wallet(self):
        """测试钱包信息"""
        user_wallet_response = self.user.wallet()
        self.assertEqual(user_wallet_response.status_code, 404)
