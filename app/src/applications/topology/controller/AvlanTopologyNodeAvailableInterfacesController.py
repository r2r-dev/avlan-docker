from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.topology.api.AvlanTopologyApi import AvlanTopologyApi
from src.applications.topology.view.AvlanTopologyNodeAvailableInterfacesView import \
    AvlanTopologyNodeAvailableInterfacesView
from webob import Response


# Open database connection
class AvlanTopologyNodeAvailableInterfacesController(AvlanAuthorizedController):
    def get(self, node_id):
        api = AvlanTopologyApi(self.dao)

        available_interfaces = api.get_node_available_interfaces(
            node_id=node_id,
        )

        # TODO: move translations handling to BaseController
        translation = list(self.request.accept_language)[0]
        view = AvlanTopologyNodeAvailableInterfacesView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._available_interfaces = available_interfaces

        response = Response()
        response.body = view.render()
        return response
