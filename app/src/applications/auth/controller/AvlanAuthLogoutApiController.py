from src.applications.auth.controller.AvlanAuthorizedController import AvlanAuthorizedController
from src.applications.auth.api.AvlanAuthApi import AvlanAuthApi


class AvlanAuthLogoutApiController(AvlanAuthorizedController):
    def get(self):
        authorization_header = self.request.authorization
        token_value = authorization_header[1]

        api = AvlanAuthApi(self.dao)
        api.invalidate_token(token_value)

        return 'Token invalidated!'
