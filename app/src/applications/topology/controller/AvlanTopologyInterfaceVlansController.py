from src.applications.auth.controller.AvlanAuthorizedController import \
    AvlanAuthorizedController
from src.applications.topology.api.AvlanTopologyApi import AvlanTopologyApi
from src.applications.topology.view.AvlanTopologyInterfaceVlansView import \
    AvlanTopologyInterfaceVlansView
from webob import Response


# Open database connection
class AvlanTopologyInterfaceVlansController(AvlanAuthorizedController):
    def get(self, interface_id):
        api = AvlanTopologyApi(self.dao)

        vlans_on_interface = api.get_interface_vlans(
            interface_id=interface_id,
        )

        # TODO: move translations handling to BaseController
        translation = list(self.request.accept_language)[0]
        view = AvlanTopologyInterfaceVlansView(
            translation=translation,
        )

        view._full = not self.request.is_xhr
        view._vlans = vlans_on_interface

        response = Response()
        response.body = view.render()
        return response
