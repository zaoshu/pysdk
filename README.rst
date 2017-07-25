# pysdk

## dome.py文件
  在dome文件中包含使用sdk的例子，只需要将api_key 与 api_secret 修改为自己的 ，便可以运行所有功能。

## zaoshu模块的构成

* zaoshuRequests : 造数HTTP库
* zaoshuSdk ：造数SDK
* Instance : 造数实例类
* User ：造数用户类

##  zaoshuRequests : 造数HTTP库

  造数HTTP库基于Requests库的基础上，添加了符合造数签名规则的函数，目前支持 GET、POST、PATCH 请求自动添加签名

##  zaoshuSdk : 造数SDK

  造数SDK 将 造数HTTP库，造数实例类，造数用户类 聚合在一起，通过 统一的对象进行使用

##  Instance : 造数实例类

  造数实例类 是对造数实例 api 功能的一个封装，大家可以直接使用函数来使用造数提供的服务

##  User ：造数用户类

  造数实例类 是对造数用户 api 功能的一个封装，大家可以直接使用函数来使用造数提供的服务

# 使用教程

## ZaoshuRequests对象是对Requests对象的请求头进行了请求头的封装
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
## 3. 用户实例, sdk
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