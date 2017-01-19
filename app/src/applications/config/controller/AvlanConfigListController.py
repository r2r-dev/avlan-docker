from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.config.view.AvlanConfigListView import AvlanConfigListView
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery

from webob import Response


# Open database connection
class AvlanConfigListController(AvlanAuthorizedController):
    def get(self):
        api = AvlanConfigApi(self.dao)
        configs = api.list_configs()

        viewer_id = self.session['user_id']
        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanConfigListView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._configs = configs

        response = Response()
        response.body = view.render()
        return response
