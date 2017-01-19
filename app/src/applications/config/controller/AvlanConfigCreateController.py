from src.applications.auth.controller.AvlanAuthorizedController import AvlanAuthorizedController
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.base.api.AvlanBaseApi import AvlanApiException
from src.applications.config.view.AvlanConfigCreateView import AvlanConfigCreateView
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery

from webob import Response


# Open database connection
class AvlanConfigCreateController(AvlanAuthorizedController):
    def get(self):
        viewer_id = self.session['user_id']
        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanConfigCreateView(
            translation=translation,
        )

        view._full = not self.request.is_xhr

        response = Response()
        response.body = view.render()
        return response

    def post(self):
        config_api = AvlanConfigApi(self.dao)
        viewer_id = self.session['user_id']
        params = self.request.params

        message = None
        error = None

        response_dict = {}
        for key, value in params.items():
            response_dict[key] = value

        try:
            config_api.create_config(
                payload=response_dict,
            )
        except AvlanApiException, e:
            error = e
        else:
            message = "Saved"

        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanConfigCreateView(
            translation=translation,
        )

        view._full = not self.request.is_xhr

        view.message = message
        view.error = error

        response = Response()
        response.body = view.render()
        return response
