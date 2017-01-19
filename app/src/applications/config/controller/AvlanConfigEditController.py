from src.applications.auth.controller.AvlanAuthorizedController import AvlanAuthorizedController
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.base.api.AvlanBaseApi import AvlanApiException
from src.applications.config.view.AvlanConfigEditView import AvlanConfigEditView
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery

from webob import Response


# Open database connection
class AvlanConfigEditController(AvlanAuthorizedController):
    def get(self, config_id):
        config_api = AvlanConfigApi(self.dao)

        viewer_id = self.session['user_id']

        config = config_api.get_config(id=config_id)

        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanConfigEditView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._config = config

        response = Response()
        response.body = view.render()
        return response
    '''

    def post(self, user_id):
        user_api = AvlanUserApi(self.dao)
        viewer_id = self.session['user_id']
        params = self.request.params

        message = None
        error = None

        response_dict = {}
        for key, value in params.items():
            response_dict[key] = value

        try:
            user_api.update_user(
                user_id=user_id,
                payload=response_dict,
            )
        except AvlanApiException, e:
            error = e
        else:
            message = "Saved"

        user = user_api.get_user(
            id=user_id,
        )

        setting_query = AvlanSettingQuery(self.dao)
        user_settings = setting_query.get_user_settings(user_id)
        allowed_settings = setting_query.get_settings()

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanUserEditView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._user = user
        view._settings = allowed_settings
        view._user_settings = user_settings

        view.message = message
        view.error = error

        response = Response()
        response.body = view.render()
        return response
'''