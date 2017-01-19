from webob import Response

from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.user.api.AvlanUserApi import AvlanUserApi
from src.applications.home.view.AvlanHomeView import AvlanHomeView
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery


# Open database connection
class AvlanHomeController(AvlanAuthorizedController):
    def get(self):
        user_id = self.session['user_id']
        user_api = AvlanUserApi(self.dao)
        user = user_api.get_user(id=user_id)

        setting_query = AvlanSettingQuery(self.dao)
        user_settings = setting_query.get_user_settings(user_id)
        translation = user_settings['language']
        view = AvlanHomeView(translation)

        view.user = user
        view._color = user_settings['color']

        response = Response()
        response.body = view.render()
        return response
