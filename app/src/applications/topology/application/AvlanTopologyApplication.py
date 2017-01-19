from src.applications.base.application.AvlanBaseApplication import\
    AvlanBaseApplication
from src.applications.topology.controller.AvlanTopologyMapController import\
    AvlanTopologyMapController
from src.applications.topology.controller.AvlanTopologyDetailController import\
    AvlanTopologyDetailController
from src.applications.topology.controller.AvlanTopologyNodeShowController import \
    AvlanTopologyNodeShowController
from src.applications.topology.controller.AvlanTopologyInterfaceVlansController import \
    AvlanTopologyInterfaceVlansController
from src.applications.topology.controller.AvlanTopologyVlanInterfacesController import \
    AvlanTopologyVlanInterfacesController
from src.applications.topology.controller.AvlanTopologyNodeCreateController import \
    AvlanTopologyNodeCreateController
from src.applications.topology.controller.AvlanTopologyEdgeCreateController import \
    AvlanTopologyEdgeCreateController
from src.applications.topology.controller.AvlanTopologyNodeDeleteController import \
    AvlanTopologyNodeDeleteController
from src.applications.topology.controller.AvlanTopologyEdgeDeleteController import \
    AvlanTopologyEdgeDeleteController
from src.applications.topology.controller.AvlanTopologyNodeAvailableInterfacesController import \
    AvlanTopologyNodeAvailableInterfacesController
from src.applications.topology.controller.AvlanTopologyInterfaceConnectionController import \
    AvlanTopologyInterfaceConnectionController


class AvlanTopologyApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'topology',
            '/topology/',
            controller=AvlanTopologyMapController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'topology',
            '/topology/{type}',
            controller=AvlanTopologyDetailController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'topology',
            '/topology/details/{node_id}',
            controller=AvlanTopologyNodeShowController,
            conditions=dict(method=["GET"]),
            action='get',
        )

        self.mapper.connect(
            'topology',
            '/topology/vlan/{vlan_id}',
            controller=AvlanTopologyVlanInterfacesController,
            conditions=dict(method=["GET"]),
            action='get',
        )

        self.mapper.connect(
            'topology',
            '/topology/interface/{interface_id}',
            controller=AvlanTopologyInterfaceVlansController,
            conditions=dict(method=["GET"]),
            action='get',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/create',
            controller=AvlanTopologyNodeCreateController,
            conditions=dict(method=["GET"]),
            action='get',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/create',
            controller=AvlanTopologyNodeCreateController,
            conditions=dict(method=["POST"]),
            action='post',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/{node_id}/edge/create',
            controller=AvlanTopologyEdgeCreateController,
            conditions=dict(method=["GET"]),
            action='get',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/{node_id}/edge/create',
            controller=AvlanTopologyEdgeCreateController,
            conditions=dict(method=["POST"]),
            action='post',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/{node_id}/delete',
            controller=AvlanTopologyNodeDeleteController,
            conditions=dict(method=["GET"]),
            action='get',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/{node_id}/delete',
            controller=AvlanTopologyNodeDeleteController,
            conditions=dict(method=["POST"]),
            action='post',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/{node_id}/edge/delete',
            controller=AvlanTopologyEdgeDeleteController,
            conditions=dict(method=["GET"]),
            action='get',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/{node_id}/edge/delete',
            controller=AvlanTopologyEdgeDeleteController,
            conditions=dict(method=["POST"]),
            action='post',
        )

        self.mapper.connect(
            'topology',
            '/topology/node/{node_id}/available_interfaces',
            controller=AvlanTopologyNodeAvailableInterfacesController,
            conditions=dict(method=["GET"]),
            action='get',
        )

        self.mapper.connect(
            'topology',
            '/topology/interface/{interface_id}/connection',
            controller=AvlanTopologyInterfaceConnectionController,
            conditions=dict(method=["GET"]),
            action='get',
        )
