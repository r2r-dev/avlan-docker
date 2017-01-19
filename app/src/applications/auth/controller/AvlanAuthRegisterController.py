from src.applications.base.controller.AvlanBaseController import AvlanBaseController
from src.applications.auth.view.AvlanAuthRegisterView import AvlanAuthRegisterView
from src.applications.auth.api.AvlanAuthApi import AvlanAuthApi
from webob import (
    exc,
    Response,
)


class AvlanAuthRegisterController(AvlanBaseController):
    def get(self):
        translation = list(self.request.accept_language)[0]
        view = AvlanAuthRegisterView(translation)
        response = Response()
        response.body = view.render()
        return response

    def post(self):
        # TODO: check whether passwords match
        params = self.request.params
        api = AvlanAuthApi(self.dao)
        response_dict = {}
        for key, value in params.items():
            response_dict[key] = value
        api_response = api.register(
            payload=response_dict,
        )

        if api_response:
            response = exc.HTTPMovedPermanently(location='/auth/login')
            return response
        else:
            response = exc.HTTPUnauthorized()
        return response
