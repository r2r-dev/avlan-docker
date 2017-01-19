from src.applications.auth.controller.AvlanAuthorizedController import\
    AvlanAuthorizedController
from src.applications.base.api.AvlanBaseApi import AvlanApiException
from src.applications.topology.api.AvlanTopologyApi import AvlanTopologyApi
from webob import Response


# Open database connection
class AvlanTopologyDetailController(AvlanAuthorizedController):
    def get(self, type):
        topology_api = AvlanTopologyApi(self.dao)
        try:
            response_dict = {}
            if type == 'nodes':
                response_dict = topology_api.get_nodes()
            elif type == 'edges':
                response_dict = topology_api.get_edges()
            elif type == 'vlans':
                response_dict = topology_api.get_vlans()
        except AvlanApiException:
            response_dict = {'Error'}

        response = Response()
        response.json_body = response_dict
        return response
