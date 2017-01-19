from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.topology.api.AvlanTopologyApi import AvlanTopologyApi
from src.applications.topology.view.AvlanTopologyNodeShowView import \
    AvlanTopologyNodeShowView
from webob import Response


# Open database connection
class AvlanTopologyNodeShowController(AvlanAuthorizedController):
    def get(self, node_id):
        api = AvlanTopologyApi(self.dao)

        node_details = api.get_node_details(
            node_id=node_id,
        )

        # TODO: move translations handling to BaseController
        translation = list(self.request.accept_language)[0]
        view = AvlanTopologyNodeShowView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._node = node_details['node']
        view._interfaces = node_details['interfaces']
        view._vlans = node_details['vlans']

        response = Response()
        response.body = view.render()
        return response
