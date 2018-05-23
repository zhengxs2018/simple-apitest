from jinja2.nodes import Output, Assign, Name, TemplateData
from jinja2.environment import Environment, TemplateExpression

env = Environment()


def compile_data(data):
    def render(context):
        if isinstance(data, str):
            value = compile_expression(data)(context)
            if has_variables(value):
                return compile_data(value)(context)

            return value

        elif isinstance(data, list):
            return [compile_data(item)(context) for item in data]

        elif isinstance(data, dict):
            return {compile_data(key)(context): compile_data(value)(context) for key, value in data.items()}
        return data

    return render


def has_variables(value):
    return isinstance(value, str) and env.variable_start_string in value and env.variable_end_string in value


def compile_expression(source):
    tpl = env.parse(source)
    if len(tpl.body) == 1 and isinstance(tpl.body[0], Output) \
            and len(tpl.body[0].nodes) == 1 and not isinstance(tpl.body[0].nodes[0], TemplateData):
        tpl.body = [Assign(Name('result', 'store'), tpl.body[0].nodes[0], lineno=1)]
        return TemplateExpression(env.from_string(tpl), True)

    return env.from_string(tpl).render


def dispatch_hook(key, hooks, hook_data=None, **kwargs):
    """Dispatches a hook dictionary on a given piece of data."""
    # like requests.hooks.dispatch_hook
    hooks = hooks or dict()
    hooks = hooks.get(key)
    if hooks:
        if hasattr(hooks, '__call__'):
            hooks = [hooks]
        for hook in hooks:
            _hook_data = hook(hook_data, **kwargs)
            if _hook_data is not None:
                hook_data = _hook_data
    return hook_data
