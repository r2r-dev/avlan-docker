from src.applications.base.controller.AvlanBaseController import AvlanBaseController
from src.applications.auth.api.AvlanAuthApi import AvlanAuthApi


# Open database connection
class AvlanAuthRegisterApiController(AvlanBaseController):
    def post(self):

        '''
        TODO: display error message if there is already user with selected name
        '''
        api = AvlanAuthApi(self.dao)
        response = api.register(
            payload=self.request.text,
        )

        return 'Response: {0:d}!'.format(response)
