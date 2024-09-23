# 超简陋的接口测试框架

项目的灵感来源于 [httprunner]，但是实现机制不一样，同时部分设定也有区别，本项目主要用于学习，
项目中推荐使用 [httprunner]。

## 运行测试

项目使用 python3 开发，不兼容 python2

```bash
# 安装依赖
$ pip install -r requirements.txt

# 运行demo
$ python runtest.py
```

## 结构说明

所有数据都可以使用 [jinja2] 的模板变量, 包括字典的 key 哦，语法为 `{{ variable }}`

```jsonc
[
  {
    // 参数化设置，可以使用的上下文变量为：globals, os.environ
    "parameters": [
      {
        "username": "admin",
        "password": "123456",
        "nickname": "超级管理员"
      },
      {
        "username": "zs",
        "password": "123456",
        "nickname": "张三"
      }
    ],
    // 局部变量，可以使用的上下文变量为：parameter， globals, os.environ
    "variables": {
      "token": "ada45sd6as5dsa"
    },
    // 测试集合名词，可以使用的上下文变量为：variables，parameter， globals, os.environ
    "name": "测试用户账号",
    
    // 全局请求接口配置，可以使用的上下文变量为：variables，parameter， globals, os.environ
    "request": {
      "base_url": "{{ BASE_URL }}",
      "headers": {},
      "cookies": {},
      // 参考 requests.request 的 hooks 参数
      "hooks": {
        "response": [
          "{{ response_hook_func }}"
        ]
      }
    },
    "tests": [
      {
      // 测试用例也支持 parameters 和 variables, 参考上面的设定
      // 测试用例名称, 上下文参考上面的设定
        "name": "测试 {{ nickname }} 登录",
        "skip": "跳过测试用例的原因",
        "skipIf": {
          "condition":true, // 支持模板表达式
          "reason": "跳过的原因"
        },
      // 测试用例钩子函数, 目前只支持 setup，teardown
        "hooks": {
          "setup": [
            "{{ setup_hook_func }}"
          ],
          "teardown": [
            "{{ teardown_hook_func }}"
          ]
        },
        // 请求接口配置，不支持 base_url, 参考 requests.request 的参数配置
        "request": {
          "url": "/get",
          "method": "GET",
          "hooks": {
            "response": [
              "{{ response_hook_func }}"
            ]
          }
        },
        "validate": [
          {
            "check": "{{ res.status_code is 200 }}",
            "message": "检查状态码是否为200"
          }
        ]
      }
    ]
  }
]
```

## 待办任务

 - [ ] 接口定义分离
 - [ ] 测试集合定义分离
 - [ ] 支持 setUpClass tearDownClass 钩子
  

## 感谢

以下排名不分先后

 - [requests]
 - [httprunner]
 - [jinja2]
 

 [httprunner]: https://github.com/httprunner/httprunner
 [requests]: http://docs.python-requests.org/zh_CN/latest/index.html
 [jinja2]: http://jinja.pocoo.org/docs/2.10/
