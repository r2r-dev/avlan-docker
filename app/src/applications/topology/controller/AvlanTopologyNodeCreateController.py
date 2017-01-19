from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.topology.view.AvlanTopologyNodeCreateView import (
    AvlanTopologyNodeCreateView
)
from src.applications.config.query.AvlanConfigQuery import AvlanConfigQuery

from webob import Response
from threading import Thread


# Open database connection
class AvlanTopologyNodeCreateController(AvlanAuthorizedController):
    def get(self):
        viewer_id = self.session['user_id']
        setting_query = AvlanSettingQuery(self.dao)

        config_query = AvlanConfigQuery(self.dao)
        node_types = config_query.get_node_types()

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanTopologyNodeCreateView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._node_types = node_types

        response = Response()
        response.body = view.render()
        return response

    def post(self):
        config_api = AvlanConfigApi(self.dao)

        config_query = AvlanConfigQuery(self.dao)
        node_types = config_query.get_node_types()

        viewer_id = self.session['user_id']
        params = self.request.params

        message = None
        error = None

        response_dict = {}
        for key, value in params.items():
            response_dict[key] = value

        '''
        Catch and log all exceptions both to GUI and console as this method
        is meant to be run as sub-thread, stopping activity indicator and
        displaying error message (if any). Communication between threads is
        handled via mutable object passed via reference (result list).
        '''
        result = []
        thread = Thread(
            target=config_api.create_node,
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
            message = "Saved"

        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanTopologyNodeCreateView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._node_types = node_types

        view.message = message
        view.error = error

        response = Response()
        response.body = view.render()
        return response
