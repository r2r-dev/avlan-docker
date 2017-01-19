from src.applications.auth.controller.AvlanAuthorizedController import AvlanAuthorizedController
from src.applications.auth.api.AvlanAuthApi import AvlanAuthApi
from webob import exc


class AvlanAuthLogoutController(AvlanAuthorizedController):
    def get(self):
        response = exc.HTTPMovedPermanently(location="/")
        api = AvlanAuthApi(self.dao)

        token_value = self.request.cookies['Token']
        api.invalidate_token(token_value)
        response.delete_cookie('Token')
        self.session.delete()
        return response
