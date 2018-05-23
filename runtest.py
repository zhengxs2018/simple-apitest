from os import environ
from json import load
from codecs import open
from collections import ChainMap
from unittest import TextTestRunner

from lib.suite import make_suites

with open('./tests/test_demo.json', encoding='utf-8') as f:
    data = load(f)


def setup_hook_func(*args, **kwargs):
    print('hooks: setup: runtest')


def response_hook_func(*args, **kwargs):
    print('hooks: response: runtest')


def teardown_hook_func(*args, **kwargs):
    print('hooks: teardown: runtest')


# 全局变量
global_variables = {
    'BASE_URL': 'https://httpbin.org',
    'setup_hook_func': setup_hook_func,
    'response_hook_func': response_hook_func,
    'teardown_hook_func': teardown_hook_func
}

# 执行上下文
context = ChainMap(global_variables, environ)

runner = TextTestRunner(verbosity=2)

# make_suites(data, context)
runner.run(make_suites(data, context))
