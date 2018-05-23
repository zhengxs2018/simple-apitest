from copy import deepcopy
from requests import request
from urllib.parse import urljoin


def _merge_settings(target: dict, src: dict):
    for key, value in src.items():
        if key in target and isinstance(value, (list, dict)) and isinstance(target[key], (list, dict)):
            if isinstance(target[key], list):
                target[key].extend(value)
            else:
                target[key] = _merge_settings(target[key], value)
        else:
            target[key] = value

    return target


class HttpClient(object):
    attributes = ('headers', 'cookies', 'auth', 'verify', 'hooks', 'cert', 'timeout', 'proxies')

    def __init__(self, base_url=None, headers=None, cookies=None, timeout=None,
                 cert=None, auth=None, hooks=None, proxies=None, verify=None):
        self.base_url = base_url
        self.headers = headers
        self.cookies = cookies
        self.auth = auth
        self.verify = verify
        self.hooks = hooks
        self.cert = cert
        self.verify = verify
        self.timeout = timeout
        self.proxies = proxies

    def _get_settings(self):
        return {name: deepcopy(getattr(self, name)) for name in self.attributes if getattr(self, name) is not None}

    def _set_settings(self, settings: dict):
        for name in self.attributes:
            if name in settings:
                setattr(self, name, settings[name])

    settings = property(_get_settings, _set_settings)

    def setup(self, target: dict, settings: dict = None):
        if isinstance(settings, dict):
            return _merge_settings(_merge_settings(target, self.settings), settings)

        else:
            settings = self.settings = _merge_settings(self.settings, target)
            return settings

    def request(self, method='GET', url='/', **kwargs):
        """Constructs and sends a :class:`Request <Request>`.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request.request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response

        Usage::

          >>> client = HttpClient('http://httpbin.org')
          >>> req = client.request('GET', '/get')
          <Response [200]>
        """
        return request(**self.setup({'method': method, 'url': urljoin(self.base_url, url)}, kwargs))

    def new_client(self, **kwargs):
        # todo: 为了避免 cookies 混淆，每个测试用例可以自由决定是否创建新的实例
        return self.__class__(**self.setup(self.settings, kwargs))
