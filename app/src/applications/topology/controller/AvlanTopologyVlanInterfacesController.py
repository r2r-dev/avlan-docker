from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.topology.api.AvlanTopologyApi import AvlanTopologyApi
from src.applications.topology.view.AvlanTopologyVlanInterfacesView import \
    AvlanTopologyVlanInterfacesView
from webob import Response


# Open database connection
class AvlanTopologyVlanInterfacesController(AvlanAuthorizedController):
    def get(self, vlan_id):
        topology_api = AvlanTopologyApi(self.dao)

        interfaces_on_vlan = topology_api.get_vlan_interfaces(
            vlan_id=vlan_id,
        )

        # TODO: move translations handling to BaseController
        translation = list(self.request.accept_language)[0]

        # TODO: this is API controller, it should not render view.
        view = AvlanTopologyVlanInterfacesView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._interfaces = interfaces_on_vlan

        response = Response()
        response.body = view.render()
        return response
