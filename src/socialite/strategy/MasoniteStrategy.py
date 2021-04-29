from social_core.strategy import BaseStrategy, BaseTemplateStrategy
from social_core.utils import build_absolute_uri

from socialite.helpers import get_config
from wsgi import container
from masonite.view import View
from masonite.response import Response
from config import socialite


class MasoniteTemplateStrategy(BaseTemplateStrategy):

    def __init__(self, strategy):
        super().__init__(strategy)
        self.view = container.make(View)
        self.response = container.make(Response)

    def render_template(self, tpl, context):
        return self.view.render(tpl).rendered_template

    def render_string(self, html, context):
        return self.response.view(html, status=200)


class MasoniteStrategy(BaseStrategy):
    DEFAULT_TEMPLATE_STRATEGY = MasoniteTemplateStrategy

    def __init__(self, storage=None, tpl=None, request=None):
        super().__init__(storage, tpl)
        self.request = request
        self.session = request.session if request else {}

    def redirect(self, url):
        return self.request.redirect(url)

    def get_setting(self, name):
        return getattr(socialite, name)

    def html(self, content):
        return self.tpl.render_string(html=content, context='')

    def request_data(self, merge=True):
        return self.request.all() if merge else {}

    def request_host(self):
        return get_config('application.URL')

    def session_get(self, name, default=None):
        value = self.session.get(name)
        return value if value else default

    def session_set(self, name, value):
        self.session.set(name, value)
        if hasattr(self.session, 'modified'):
            self.session.set('modified', True)
        return value

    def session_pop(self, name):
        self.session.pop(name)

    def build_absolute_uri(self, path=None):
        host_url = self.request_host()
        if self.request:
            if not host_url.endswith('/'):
                host_url += '/'
            path = build_absolute_uri(host_url, path)
        return path

    def request_is_secure(self):
        host_url = self.request_host()
        return host_url.startswith('https://')

    def request_path(self):
        return self.request.path

    def request_port(self):
        return self.request.environ.get('SERVER_PORT')

    def request_get(self):
        return self.request_data()

    def request_post(self):
        return self.request_data()

    def authenticate(self, backend, *args, **kwargs):
        response = kwargs.get('response')
        user = backend.get_user_details(response)
        return user, response
