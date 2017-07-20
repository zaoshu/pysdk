# pysdk 

## zaoshu模块的构成

* zaoshuRequests : 造数HTTP库
* zaoshuSdk ：造数SDK
* Instance : 造数实例类
* User ：造数用户类
* 测试用例

##  zaoshuRequests : 造数HTTP库

  造数HTTP库基于Requests库的基础上，添加了符合造数签名规则的函数，目前支持 GET、POST、PATCH 请求自动添加签名


##  zaoshuSdk : 造数SDK
  造数SDK 将 造数HTTP库，造数实例类，造数用户类 聚合在一起，通过 统一的对象进行使用

##  Instance : 造数实例类
  造数实例类 是对造数实例 api 功能的一个封装，大家可以直接使用函数来使用造数提供的服务

##  User ：造数用户类
  造数实例类 是对造数用户 api 功能的一个封装，大家可以直接使用函数来使用造数提供的服务

## 测试用例
  测试用例中,添加上 自己的  api_key 与 api_secret ，便可以运行所有功能
