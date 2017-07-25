#!/usr/bin.env python3
# coding=utf-8

"""
造数模块的单元测试
"""
import unittest
import requests
from zaoshu import ZaoshuRequests
from zaoshu import ZaoshuSdk
from zaoshu import Instance
from zaoshu import User

class TestZaoshuRequests(unittest.TestCase):
    """
    造数Http库ZaoshuRequests单元测试
    """
    def setUp(self):
        self.api_key = 'ca3a56bdb5594c2b9e6d3f87f3d35baf'
        self.api_secret = '80518755f8d5d91f730a9332e2941023e41e29a856e6285bf51901af2f50f2b0'
        self.request = ZaoshuRequests(self.api_key, self.api_secret)

    def test_sign(self):
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
        query = {
            'a': '1',
            'b': '2',
        }

        body = '{"v":"tt"}'
        methods = 'POST'

        headers = self.request.get_headers(method=methods, query=query, body=body)
        self.assertNotEqual(headers['Authorization'], '')
        self.assertEqual(headers['Content-Type'],'application/json; charset=utf-8')

    def test_get(self):
        base_url = 'https://openapi.zaoshu.io/v2'

        get_request = self.request.get(base_url)
        self.assertTrue(isinstance(get_request, requests.models.Response))


class TestZaoshuSdk(unittest.TestCase):
    """
    造数SDK ZaoshuSdk 单元测试
    """

    def setUp(self):
        self.api_key = 'ca3a56bdb5594c2b9e6d3f87f3d35baf'
        self.api_secret = '80518755f8d5d91f730a9332e2941023e41e29a856e6285bf51901af2f50f2b0'
        self.sdk = ZaoshuSdk(self.api_key, self.api_secret)

    def test(self):
        sdk = ZaoshuSdk(self.api_key, self.api_secret)

        self.assertTrue(isinstance(sdk.request, ZaoshuRequests))
        self.assertTrue(isinstance(sdk.instance, Instance))
        self.assertTrue(isinstance(sdk.user, User))

class TestInstance(unittest.TestCase):
    """
    造数 实例 Instance 单元测试
    """

    def setUp(self):
        self.api_key = 'ca3a56bdb5594c2b9e6d3f87f3d35baf'
        self.api_secret = '80518755f8d5d91f730a9332e2941023e41e29a856e6285bf51901af2f50f2b0'
        self.request = ZaoshuRequests(self.api_key, self.api_secret)
        self.base_url = 'https://openapi.zaoshu.io/v2'
        self.instance = Instance(self.base_url, self.request)
        self.instance_id = '7139aa25d85141829e4faf28ea551226'
        self.task_id = '48607ed016fe4b1fb19069b2b5430d59'

    def test_1_list(self):
        # 获取用户的爬虫实例
        instance_list_response = self.instance.list()
        self.assertEqual(instance_list_response.status_code, 200)
        self.instance_id = instance_list_response.json()['data'][0]['id']

    def test_2_item(self):
        self.assertNotEqual(self.instance_id, '')
        instance_item_response = self.instance.item(self.instance_id)
        self.assertEqual(instance_item_response.status_code, 200)

    def test_3_schema(self):
        instance_schema_response = self.instance.schema(self.instance_id)
        self.assertEqual(instance_schema_response.status_code, 200)

    def test_4_edit(self):
        instance_edit_response = self.instance.edit(self.instance_id, title='测试修改实例数据标题')
        self.assertEqual(instance_edit_response.status_code, 200)

    def test_5_run(self):
        instance_run_response = self.instance.run(self.instance_id)
        self.assertEqual(instance_run_response.status_code, 200)

    def test_6_task_list(self):
        instance_task_list_response = self.instance.task_list(self.instance_id)
        self.assertEqual(instance_task_list_response.status_code, 200)
        self.task_id = instance_task_list_response.json()['data'][-1]['id']

    def test_7_task(self):
        instance_task_response = self.instance.task(self.instance_id, self.task_id)
        self.assertEqual(instance_task_response.status_code, 200)

    def test_8_download_run_data(self):
        instance_download_path = self.instance.download_run_data(self.instance_id,
                                                                self.task_id,
                                                                file_type='json')
        self.assertNotEqual(instance_download_path, "")


class TestUser(unittest.TestCase):
    
    def setUp(self):
        self.api_key = 'ca3a56bdb5594c2b9e6d3f87f3d35baf'
        self.api_secret = '80518755f8d5d91f730a9332e2941023e41e29a856e6285bf51901af2f50f2b0'
        self.request = ZaoshuRequests(self.api_key, self.api_secret)
        self.base_url = 'https://openapi.zaoshu.io/v2'
        self.user = User(self.base_url, self.request)

    def test_account(self):
        user_account_response = self.user.account()
        self.assertEqual( user_account_response.status_code, 200)

    def test_wallet(self):
        user_wallet_response = self.user.wallet()
        self.assertEqual( user_wallet_response.status_code, 200)