from webob import (
    exc,
    Response,
)


class AvlanBaseController(object):
    special_vars = (
        'controller',
        'action',
    )

    def __init__(self, request, link, **config):
        self.request = request
        self.link = link
        self.session = self.request.environ['beaker.session']
        for name, value in config.items():
            setattr(
                self,
                name,
                value,
            )

    def __call__(self):
        try:
            '''
            Execute pre-response if available
            '''
            if hasattr(
                self,
                '__before__',
            ):
                pre_response = self.__before__()

                # TODO: extract additional data from pre_response
                # i.e. logged user id based on passed token
                # display pre-response if it failed
                if pre_response.status_code != 200:
                    return pre_response

            action = self.request.urlvars.get('action')
            kwargs = self.request.urlvars.copy()
            for attr in self.special_vars:
                if attr in kwargs:
                    del kwargs[attr]
            try:
                response = getattr(
                    self,
                    action,
                )(**kwargs)
            except AttributeError, e:
                raise exc.HTTPNotFound("No action {0:s}".format(action))
            if isinstance(
                    response,
                    basestring,
            ):
                response = Response(body=response)
        except exc.HTTPException, e:
            response = e
        return response
