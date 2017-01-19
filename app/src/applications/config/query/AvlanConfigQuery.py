from src.applications.base.query.AvlanBaseQuery import AvlanBaseQuery
from src.applications.config.storage.AvlanConfigStorage import \
    AvlanConfigStorage
from src.applications.config.storage.AvlanNodeStorage import \
    AvlanNodeStorage
from src.applications.config.storage.AvlanNodeTypeStorage import \
    AvlanNodeTypeStorage
from src.applications.config.storage.AvlanInterfaceStorage import \
    AvlanInterfaceStorage
from src.applications.config.storage.AvlanVlanStorage import \
    AvlanVlanStorage
from src.applications.config.storage.AvlanInterfaceVlanStorage import \
    AvlanInterfaceVlanStorage


class AvlanConfigQuery(AvlanBaseQuery):
    def remove_nodes(self):
        self._dao.delete_all(AvlanNodeStorage)

    def remove_interfaces(self):
        self._dao.delete_all(AvlanInterfaceStorage)

    def remove_vlans(self):
        self._dao.delete_all(AvlanVlanStorage)
        self._dao.delete_all(AvlanInterfaceVlanStorage)

    def create_node(self, name, type, ipAddress, sshPort, sshUsername,
                    sshPassword,
                    id=None):

        node = AvlanNodeStorage()
        node.id = id
        node.name = name
        node.type = type
        node.ipAddress = ipAddress
        node.sshPort = sshPort
        node.sshUsername = sshUsername
        node.sshPassword = sshPassword
        self._dao.save(node)
        return node

    def create_interface(self, id, nodeId, ifaceIndex=None,
                         peerNodeId=None, peerIfaceId=None, mac=None):
        interface = AvlanInterfaceStorage()
        interface.id = id
        interface.nodeId = nodeId
        interface.ifaceIndex = ifaceIndex
        interface.peerNodeId = peerNodeId
        interface.peerIfaceId = peerIfaceId
        interface.mac = mac
        self._dao.save(interface)

        return interface

    def create_vlan(self, vlan_number, node_id, vlan_name=None):
        vlan = AvlanVlanStorage()
        vlan.number = vlan_number
        vlan.nodeId = node_id
        vlan.name = vlan_name

        self._dao.save(vlan)
        return vlan

    def create_interface_vlan(self, ifaceId, vlanId, pvid=None):
        interface_vlan = AvlanInterfaceVlanStorage()
        interface_vlan.ifaceId = ifaceId
        interface_vlan.vlanId = vlanId
        interface_vlan.pvid = pvid
        self._dao.save(interface_vlan)

        return interface_vlan

    def create_config(self, title):
        config = AvlanConfigStorage()
        config.title = title
        self._dao.save(config)
        return config

    def get_config(self, **kwargs):
        conditions = []
        values = []
        for key, value in kwargs.items():
            condition = "{0:s} = %s".format(key)
            conditions.append(condition)
            values.append(value)
        where_clause = " AND ".join(conditions)
        configs = self._dao.list_where(
            where_clause=where_clause,
            clazz=AvlanConfigStorage,
            arg_list=values
        )

        # TODO check if unique results
        if len(configs) > 0:
            return configs[0]
        return None

    def get_nodes(self, **kwargs):
        if len(kwargs) == 0:
            example_object = AvlanNodeStorage()
            nodes = self._dao.list(example_object)
        else:
            conditions = []
            values = []
            for key, value in kwargs.items():
                condition = "{0:s} = %s".format(key)
                conditions.append(condition)
                values.append(value)
            where_clause = " AND ".join(conditions)
            nodes = self._dao.list_where(
                where_clause=where_clause,
                clazz=AvlanNodeStorage,
                arg_list=values
            )
        return nodes

    def get_interfaces(self, **kwargs):
        if len(kwargs) == 0:
            example_object = AvlanInterfaceStorage()
            interfaces = self._dao.list(example_object)
        else:
            conditions = []
            values = []
            for key, value in kwargs.items():
                condition = "{0:s} = %s".format(key)
                conditions.append(condition)
                values.append(value)
            where_clause = " AND ".join(conditions)
            interfaces = self._dao.list_where(
                where_clause=where_clause,
                clazz=AvlanInterfaceStorage,
                arg_list=values
            )
        return interfaces

    def get_interface_vlans(self, **kwargs):
        if len(kwargs) == 0:
            example_object = AvlanInterfaceVlanStorage()
            interface_vlans = self._dao.list(example_object)
        else:
            conditions = []
            values = []
            for key, value in kwargs.items():
                condition = "{0:s} = %s".format(key)
                conditions.append(condition)
                values.append(value)
            where_clause = " AND ".join(conditions)
            interface_vlans = self._dao.list_where(
                where_clause=where_clause,
                clazz=AvlanInterfaceVlanStorage,
                arg_list=values
            )
        return interface_vlans

    def get_vlan_interfaces(self, **kwargs):
        if len(kwargs) == 0:
            example_object = AvlanInterfaceVlanStorage()
            vlan_interfaces = self._dao.list(example_object)
        else:
            conditions = []
            values = []
            for key, value in kwargs.items():
                condition = "{0:s} = %s".format(key)
                conditions.append(condition)
                values.append(value)
            where_clause = " AND ".join(conditions)
            vlan_interfaces = self._dao.list_where(
                where_clause=where_clause,
                clazz=AvlanInterfaceVlanStorage,
                arg_list=values
            )
        return vlan_interfaces

    def get_vlans(self, **kwargs):
        if len(kwargs) == 0:
            example_object = AvlanVlanStorage()
            vlans = self._dao.list(example_object)
        else:
            conditions = []
            values = []
            for key, value in kwargs.items():
                condition = "{0:s} = %s".format(key)
                conditions.append(condition)
                values.append(value)
            where_clause = " AND ".join(conditions)
            vlans = self._dao.list_where(
                where_clause=where_clause,
                clazz=AvlanVlanStorage,
                arg_list=values
            )
        return vlans

    def get_node_types(self, **kwargs):
        if len(kwargs) == 0:
            example_object = AvlanNodeTypeStorage()
            node_types = self._dao.list(example_object)
        else:
            conditions = []
            values = []
            for key, value in kwargs.items():
                condition = "{0:s} = %s".format(key)
                conditions.append(condition)
                values.append(value)
            where_clause = " AND ".join(conditions)
            node_types = self._dao.list_where(
                where_clause=where_clause,
                clazz=AvlanVlanStorage,
                arg_list=values
            )
        return node_types
