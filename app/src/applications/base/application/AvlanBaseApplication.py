from abc import (
    ABCMeta,
    abstractmethod,
)
from routes import (
    Mapper,
    URLGenerator,
)
from webob import exc
from webob.dec import wsgify


class AvlanBaseApplication(object):
    __metaclass__ = ABCMeta

    def __init__(self, **config):
        self.config = config
        self.mapper = Mapper()
        self._set_routes()

    @abstractmethod
    def _set_routes(self):
        pass

    @wsgify
    def __call__(self, request):
        results = self.mapper.routematch(environ=request.environ)
        if not results:
            return exc.HTTPNotFound()
        (
            match,
            route,
        ) = results
        request.urlvars = match

        return self._get_route(
            match=match,
            request=request,
        )

    def _get_route(self, **kwargs):
        match = kwargs['match']
        request = kwargs['request']
        link = URLGenerator(
            self.mapper,
            request.environ,
        )
        controller = match['controller'](
            request,
            link,
            **self.config
        )
        return controller()
