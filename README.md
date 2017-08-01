# pysdk 造数Python版本SDK
## 简介
 zaoshu 是对造数openAPI接口的一层封装实现，使用户更专注于功能，而不必关注底层实现，这些SDK帮你完成。
## pip 安装造数模块
```
pip install zaoshu
```

## pip 安装完成后引入ZaoshuSdk，即可使用
```
from zaoshu.zaoshu import ZaoshuSdk

# 测试代码 部分
if __name__ == '__main__':

    ZAOSHU_URL = 'https://openapi.zaoshu.io/v2'

    # api_key = '你的api_key'
    API_KEY = '你的api_key'

    # api_secret = '你的api_secret'
    API_SERVER = '你的api_secret'

    sdk = ZaoshuSdk(API_KEY, API_SERVER, base_url=ZAOSHU_URL)
    # 造数Http类对象
    sdk.request
    # 造数实例类对象
    sdk.instance
    # 造数用户类对象
    sdk.user
	
```

## sdk功能
### http类对象功能
 - 发送 带造数签名的 GET请求
 - 发送 带造数签名的 POST请求
 - 发送 带造数签名的 PATCH请求
 
### 造数实例对象
 - 获取用户的爬虫实例列表
 - 获取实例详情
 - 获取实例的数据格式
 - 编辑实例
 - 获取实例下的任务列表
 - 运行实例
 - 获取实例下的任务详情
 - 下载实例下任务数据
 
### 造数用户对象
 - 获取用户账户信息 
 - 获取用户钱包信息
 
 
## zaoshu模块的构成

* zaoshuRequests : 造数HTTP库
* zaoshuSdk ：造数SDK
* Instance : 造数实例类
* User ：造数用户类

###  zaoshuRequests : 造数HTTP库

  造数HTTP库基于Requests库的基础上，添加了符合造数签名规则的函数，目前支持 GET、POST、PATCH 请求自动添加签名
  
   - **发送 带造数签名的 GET请求**
   
```
zaoshuRequests.get(self, url, params=None):
"""
get请求
:param url: 请求url
:param params: 请求参数
:return:requests.request
"""
```
  
   - **发送 带造数签名的 POST请求**
   
```
zaoshuRequests.post(self, url, params=None, body=None):
"""
post请求
:param url:请求url
:param params:请求参数
:param body:内容
:return:requests.request 对象
"""
  ```
  
   - **发送 带造数签名的 PATCH请求**
   
```
zaoshuRequests.patch(self, url, params=None, body=None):
"""
patch请求
:param url:请求url
:param params:请求参数
:param body:内容
:return:requests.request
"""
```
  - **requests.Response**
  
  requests.Response 的详细文档见 http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
  
  
 
###  zaoshuSdk : 造数SDK

  造数SDK 将 造数HTTP库，造数实例类，造数用户类 聚合在一起，通过 统一的对象进行使用
  - **zaoshuSdk的属性代码**
```
self.request = ZaoshuRequests(api_key, api_secret)
self.instance = Instance(self._base_url, self.request)
self.user = User(self._base_url, self.request)
```
 

###  Instance : 造数实例类

  造数实例类 是对造数实例 api 功能的一个封装，大家可以直接使用函数来使用造数提供的服务
  - **获取用户的爬虫实例列表**
  
```
Instance.list(self):
"""
获取实例列表
:return: requests.Response
"""
```
  
  - **获取实例详情**
  
```
Instance.item(self, instance_id):
"""
获取实例详情
:param instance_id: 运行实例的id编号，可以从实例列表中获取
:return: requests.Response
"""
```
  
  - **获取实例的数据格式**
  
```
Instance.schema(self, instance_id):
"""
获取单个实例的数据格式
:param instance_id:
:return: requests.Response
"""
```
  
  - **获取某实例下的任务列表**
  
```
Instance.task(self, instance_id, task_id):
"""
获取某实例下，单个任务详情
:param instance_id:
:param task_id:
:return: requests.Response
"""
  ```
  - **下载运行结果数据**
  
```
Instance.download_run_data(self, instance_id, task_id, file_type='csv', save_file=False):
"""
下载运行结果
:param instance_id: 实例ID
:param task_id: 任务ID
:param file_type: 文件类型
:param save_file: 是否保持文件
:return:保存文件的路径/BytesIO对象
"""
   ```
   
   - **运行实例**
   
```
Instance.run(self, instance_id, body=None):
"""
运行实例
:param instance_id: 运行实例的id编号，可以从实例列表中获取
:return: requests.Response
"""
```
   
   - **编辑实例**
   
```
Instance.edit(self, instance_id, title=None, result_notify_uri=None):
"""
实例编辑
:param instance_id: 实例id
:param title: 要修改的实例标题
:param result_notify_uri: 回调url
:return:requests.Response
"""
```

###  User ：造数用户类

  造数实例类 是对造数用户 api 功能的一个封装，大家可以直接使用函数来使用造数提供的服务
  
  - **获得用户帐号信息**
  
```
User.account(self):
"""
获得用户帐号信息
:return:requests.Response
"""
```
  
  - **获取用户钱包信息**
  
```
User.wallet(self):
"""
获得用户钱包信息
:return:requests.Response
"""
 ```


# 使用教程DEMO详解

## ZaoshuRequests对象
   ZaoshuRequests对象是对Requests对象的请求头进行了请求头的封装。
   可以使用Requests的方法和属性
   
   Requests.url : 请求网址
   
   Requests.status_code  ： 请求响应代码
   
   Requests.text ： 请求响应内容
   
  
## 公共函数，输出请求信息，参数为response对象

```
def print_resopnse_info(response, title=''):
    """
    输出响应信息
    :param response:response响应对象
    :param title: 显示标题
    :return: None
    """
    print('====[%s]========================================'% title)
    print("URL："+response.url)
    print("状态："+str(response.status_code))
    print("返回内容："+response.text)
    print("返回头信息：", end='')
    print(response.headers)
    print('\n')

```


## 1. 创建ZaoshuSdk的实例
```
    # 造数api链接
    ZAOSHU_URL = 'https://openapi.zaoshu.io/v2'

    # api_key = '你的api_key'
    API_KEY = '你的api_key'

    # api_secret = '你的api_secret'
    API_SERVER = '你的api_secret'

    sdk = ZaoshuSdk(API_KEY, API_SERVER, base_url=ZAOSHU_URL)

```


## 2. 用户信息, sdk.user是用户信息模块对象
```
    # 获取用户账户信息
    user_account_response = sdk.user.account()
    print_resopnse_info(user_account_response, '获取用户账户信息')

    # 获取用户钱包信息
    user_wallet_response = sdk.user.wallet()
    print_resopnse_info(user_wallet_response, '获取用户钱包信息')
```
## 3. 用户实例, sdk.instance
```
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

```
