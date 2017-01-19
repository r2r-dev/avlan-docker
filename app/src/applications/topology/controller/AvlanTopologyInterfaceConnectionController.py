from src.applications.auth.controller.AvlanAuthorizedController import\
    AvlanAuthorizedController
from src.applications.base.api.AvlanBaseApi import AvlanApiException
from src.applications.topology.api.AvlanTopologyApi import AvlanTopologyApi
from webob import Response


# Open database connection
class AvlanTopologyInterfaceConnectionController(AvlanAuthorizedController):
    def get(self, interface_id):
        topology_api = AvlanTopologyApi(self.dao)
        try:
            response_dict = topology_api.get_interface_connection(interface_id)
        except AvlanApiException:
            response_dict = {'Error'}

        response = Response()
        response.json_body = response_dict
        return response
