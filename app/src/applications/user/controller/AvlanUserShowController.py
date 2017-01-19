from src.applications.auth.controller.AvlanAuthorizedController import AvlanAuthorizedController
from src.applications.user.api.AvlanUserApi import AvlanUserApi
from src.applications.user.view.AvlanUserShowView import AvlanUserShowView
from webob import Response


# Open database connection
class AvlanUserShowController(AvlanAuthorizedController):
    def get(self, user_id):
        api = AvlanUserApi(self.dao)

        user = api.get_user(
            id=user_id,
        )

        # TODO: move translations handling to BaseController
        translation = list(self.request.accept_language)[0]
        view = AvlanUserShowView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._user = user

        response = Response()
        response.body = view.render()
        return response
