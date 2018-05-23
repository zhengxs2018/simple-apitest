from collections import ChainMap
from unittest.suite import TestSuite

from .httpclient import HttpClient
from .case import make_testcase
from .utils import compile_data


def make_suites(suites: list, context: ChainMap):
    suite = TestSuite()

    for item in suites:
        # 编译数据
        parameters = compile_data(item.get('parameters', [{}]))
        variables = compile_data(item.get('variables', {}))
        request_settings = compile_data(item.get('request', {}))

        # 参数化处理
        for parameter in parameters(context):
            # 创建子上下文
            child_context = context.new_child(parameter)

            # 将变量合并到子上下文中
            child_context.update(variables(child_context))

            # 创建 http 客户端
            client = HttpClient(**request_settings(child_context))

            # 添加集合
            suite.addTest(make_suite(item, context=child_context, client=client))

    return suite


def make_suite(model: dict, context: ChainMap = None, client: HttpClient = None) -> TestSuite:
    suite = TestSuite()

    suite.name = compile_data(model.get('name', ''))(context)

    for item in model.get('tests', []):
        # 编译数据
        parameters = compile_data(item.get('parameters', [{}]))
        variables = compile_data(item.get('variables', {}))

        # 参数化处理
        for parameter in parameters(context):
            # 创建子上下文
            child_context = context.new_child(parameter)

            # 合并变量
            child_context.update(variables(child_context))

            # 创建测试用例
            suite.addTest(make_testcase(item, client=client, context=child_context, parent=suite))

    return suite
