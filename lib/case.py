from functools import wraps
from collections import ChainMap
from unittest.case import FunctionTestCase, SkipTest, expectedFailure
from unittest.suite import TestSuite

from .utils import dispatch_hook, compile_data
from .httpclient import HttpClient


def skip(reason):
    """
    Unconditionally skip a test.
    """
    if reason is None:
        return lambda x: x

    def decorator(test_item):
        if not isinstance(test_item, type):
            @wraps(test_item)
            def skip_wrapper(*args, **kwargs):
                raise SkipTest(reason)

            test_item = skip_wrapper

        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = reason
        return test_item

    return decorator


def skip_if(condition, reason=''):
    """
    Skip a test if the condition is true.
    """
    if condition is None:
        return lambda x: x

    if isinstance(condition, list):
        condition, reason = condition

    elif isinstance(condition, dict):
        reason = condition['reason']
        condition = condition['condition']

    if condition:
        return skip(reason)

    return lambda x: x


def expected_failure(condition):
    if not condition:
        return lambda x: x

    return expectedFailure


def make_testcase(model: dict, client: HttpClient = None,
                  context: ChainMap = None, parent: TestSuite = None) -> FunctionTestCase:
    hooks = compile_data(model.get('hooks', {}))(context)
    request_settings = compile_data(model.get('request', {}))(context)
    validates = [
        {key: compile_data(value) for key, value in validate.items()}
        for validate in model.get('validate', [])
    ]

    # 拼接名称
    name = '{} / {}'.format(parent.name, compile_data(model.get('name', ''))(context))

    def setup():
        dispatch_hook('setup', hooks)

    @skip(compile_data(model.get('skip'))(context))
    @skip_if(compile_data(model.get('skipIf'))(context))
    # @expected_failure(compile_data(model.get('expectedFailure'))(context))
    def test_func():
        res = client.request(**request_settings)

        # 非 200 直接抛错
        res.raise_for_status()

        # 创建一个执行上下文
        eval_ctx = context.new_child({'res': res})

        # 验证接口
        for validate in validates:
            assert validate['check'](eval_ctx), validate['message'](eval_ctx)

    def teardown():
        dispatch_hook('teardown', hooks)

    return FunctionTestCase(testFunc=test_func, setUp=setup, tearDown=teardown, description=name)
