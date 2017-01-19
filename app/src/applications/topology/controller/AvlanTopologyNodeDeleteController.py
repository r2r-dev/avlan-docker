from src.applications.auth.controller.AvlanAuthorizedController import AvlanAuthorizedController
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.base.api.AvlanBaseApi import AvlanApiException
from src.applications.topology.view.AvlanTopologyNodeDeleteView import AvlanTopologyNodeDeleteView
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery
from src.applications.base.view.AvlanResponseView import (
    AvlanResponseView
)
from src.applications.config.query.AvlanConfigQuery import AvlanConfigQuery

from webob import Response
from threading import Thread


# Open database connection
class AvlanTopologyNodeDeleteController(AvlanAuthorizedController):
    def get(self, node_id):
        viewer_id = self.session['user_id']
        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanTopologyNodeDeleteView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._node_id = node_id

        response = Response()
        response.body = view.render()
        return response

    def post(self, node_id):
        config_api = AvlanConfigApi(self.dao)

        viewer_id = self.session['user_id']
        params = self.request.params

        message = None
        error = None

        response_dict = {}
        for key, value in params.items():
            response_dict[key] = value
        response_dict['node_id'] = node_id

        '''
        Catch and log all exceptions both to GUI and console as this method
        is meant to be run as sub-thread, stopping activity indicator and
        displaying error message (if any). Communication between threads is
        handled via mutable object passed via reference (result list).
        '''
        result = []
        thread = Thread(
            target=config_api.delete_node,
            args=(
                response_dict,
                result,
            )
        )
        thread.start()
        thread.join()
        if len(result) == 1:
            error = "Error: {0:s}".format(result[0])
        else:
            message = "Deleted"

        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanResponseView(
            translation=translation,
        )

        view._full = not self.request.is_xhr

        view.message = message
        view.error = error

        response = Response()
        response.body = view.render()
        return response
