from src.applications.auth.controller.AvlanAuthorizedController import AvlanAuthorizedController
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.config.view.AvlanConfigLoadView import (
    AvlanConfigLoadView
)
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery

from webob import Response
from threading import Thread


# Open database connection
class AvlanConfigLoadController(AvlanAuthorizedController):
    def get(self, config_id):
        config_api = AvlanConfigApi(self.dao)
        viewer_id = self.session['user_id']

        message = None
        error = None

        '''
        Catch and log all exceptions both to GUI and console as this method
        is meant to be run as sub-thread, stopping activity indicator and
        displaying error message (if any). Communication between threads is
        handled via mutable object passed via reference (result list).
        '''
        result = []
        thread = Thread(
            target=config_api.load_config,
            args=(
                config_id,
                result,
            )
        )
        thread.start()
        thread.join()
        if len(result) == 1:
            error = "Error: {0:s}".format(result[0])
        else:
            message = "Success"

        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanConfigLoadView(
            translation=translation,
        )

        view._full = not self.request.is_xhr

        view.message = message
        view.error = error
        view._config_id = config_id

        response = Response()
        response.body = view.render()
        return response
