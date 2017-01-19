from src.applications.base.controller.AvlanBaseController import AvlanBaseController
from src.applications.auth.api.AvlanAuthApi import AvlanAuthApi


# Open database connection
class AvlanAuthLoginApiController(AvlanBaseController):
    def post(self):

        api = AvlanAuthApi(self.dao)
        user_id, token_value = api.login(
            payload=self.request.text,
        )

        return token_value
