from src.applications.auth.controller.AvlanAuthorizedController import\
    AvlanAuthorizedController
from src.applications.user.api.AvlanUserApi import AvlanUserApi
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery
from src.applications.user.view.AvlanUserListView import AvlanUserListView
from webob import Response


# Open database connection
class AvlanUserListController(AvlanAuthorizedController):
    def get(self):
        api = AvlanUserApi(self.dao)
        users = api.list_users()

        setting_query = AvlanSettingQuery(self.dao)
        users_settings = {}
        for user in users:
            users_settings[user.id] = setting_query.get_user_settings(user.id)

        # TODO: move translations handling to BaseController
        translation = list(self.request.accept_language)[0]
        view = AvlanUserListView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._users = users
        view._users_settings = users_settings

        response = Response()
        response.body = view.render()
        return response
