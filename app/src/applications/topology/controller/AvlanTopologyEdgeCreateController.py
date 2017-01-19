from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.topology.view.AvlanTopologyEdgeCreateView import (
    AvlanTopologyEdgeCreateView
)
from src.applications.base.view.AvlanResponseView import (
    AvlanResponseView
)
from src.applications.config.query.AvlanConfigQuery import AvlanConfigQuery

from webob import Response
from threading import Thread


# Open database connection
class AvlanTopologyEdgeCreateController(AvlanAuthorizedController):
    def __extract_details(self, node_id, config_query):
        source_node_interfaces = config_query.get_interfaces(
            nodeId=node_id,
        )

        node_id = int(node_id)

        # Filter out interfaces with connections
        available_interfaces = []
        for source_node_interface in source_node_interfaces:
            # maybe null...
            peer_node_id = source_node_interface.peerNodeId
            if peer_node_id is None or peer_node_id == 0:
                available_interfaces.append(source_node_interface)

        target_nodes = config_query.get_nodes()

        source_node = None
        source_node_index = None
        for step in range(
                0,
                len(target_nodes),
        ):
            if target_nodes[step].id == node_id:
                source_node_index = step
                break
        if source_node_index is not None:
            source_node = target_nodes[source_node_index]
            del target_nodes[source_node_index]

        return dict(
            source_node=source_node,
            source_interfaces=available_interfaces,
            target_nodes=target_nodes,
        )

    def get(self, node_id):
        viewer_id = self.session['user_id']
        setting_query = AvlanSettingQuery(self.dao)

        config_query = AvlanConfigQuery(self.dao)
        details = self.__extract_details(
            node_id,
            config_query,
        )

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanTopologyEdgeCreateView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._source_node = details['source_node']
        view._source_interfaces = details['source_interfaces']
        view._target_nodes = details['target_nodes']

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

        '''
        Catch and log all exceptions both to GUI and console as this method
        is meant to be run as sub-thread, stopping activity indicator and
        displaying error message (if any). Communication between threads is
        handled via mutable object passed via reference (result list).
        '''
        result = []
        thread = Thread(
            target=config_api.create_edge,
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
        view = AvlanResponseView(
            translation=translation,
        )

        view._full = not self.request.is_xhr

        view.message = message
        view.error = error

        response = Response()
        response.body = view.render()
        return response
