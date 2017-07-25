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
