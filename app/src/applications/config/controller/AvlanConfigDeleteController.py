from src.applications.auth.controller.AvlanAuthorizedController import AvlanAuthorizedController
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.base.api.AvlanBaseApi import AvlanApiException
from src.applications.config.view.AvlanConfigDeleteView import AvlanConfigDeleteView
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery


from webob import Response


# Open database connection
class AvlanConfigDeleteController(AvlanAuthorizedController):
    def get(self, config_id):
        config_api = AvlanConfigApi(self.dao)
        setting_query = AvlanSettingQuery(self.dao)

        viewer_id = self.session['user_id']

        config = config_api.get_config(id=config_id)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanConfigDeleteView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._config_id = config.id

        response = Response()
        response.body = view.render()
        return response

    def post(self, config_id):
        config_api = AvlanConfigApi(self.dao)
        viewer_id = self.session['user_id']
        params = self.request.params

        message = None
        error = None

        response_dict = {}
        for key, value in params.items():
            response_dict[key] = value

        try:
            config_api.delete_config(
                id=config_id,
            )
        except AvlanApiException, e:
            error = e
        else:
            message = "Deleted"

        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanConfigDeleteView(
            translation=translation,
        )

        view._full = not self.request.is_xhr

        view.message = message
        view.error = error
        view._config_id = config_id

        response = Response()
        response.body = view.render()
        return response
