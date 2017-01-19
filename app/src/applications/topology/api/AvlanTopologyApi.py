from src.applications.base.api.AvlanBaseApi import AvlanBaseApi
from src.applications.config.query.AvlanConfigQuery import AvlanConfigQuery


class AvlanTopologyApi(AvlanBaseApi):
    def get_node_details(self, node_id):
        config_query = AvlanConfigQuery(self._dao)
        node = config_query.get_nodes(
            id=node_id
        )
        interfaces = config_query.get_interfaces(
            nodeId=node_id,
        )

        vlans = config_query.get_vlans(
            nodeId=node_id,
        )

        return dict(
            node=node[0],
            interfaces=interfaces,
            vlans=vlans,
        )

    def get_interface_connection(self, interface_id):
        config_query = AvlanConfigQuery(self._dao)

        return_dict = dict(
            empty=False
        )

        try:
            connected_interface = config_query.get_interfaces(
                peerIfaceId=interface_id,
            )[0]
        except IndexError:
            return_dict['empty'] = True
            return return_dict

        connected_node = config_query.get_nodes(
            id=connected_interface.nodeId
        )[0]

        return_dict = {
            'interface_name': connected_interface.ifaceIndex,
            'interface_id': connected_interface.id,
            'node_name': connected_node.name,
            'node_id': connected_node.id,
            'empty': False,
        }

        return return_dict

    def get_vlan_interfaces(self, vlan_id):
        config_query = AvlanConfigQuery(self._dao)
        interfaces_on_vlan = config_query.get_vlan_interfaces(
            vlanId=vlan_id,
        )

        '''
        TODO: resolve this by join in db
        TODO: pass nodeId to reduce amount of results
        '''
        complete_interface_list = []
        interfaces = config_query.get_interfaces()
        for interface_on_vlan in interfaces_on_vlan:
            for interface in interfaces:
                if interface_on_vlan.ifaceId == interface.id:
                    if interface_on_vlan.pvid == 1:
                        is_pvid = 'True'
                    else:
                        is_pvid = ''
                    response_dict = dict(
                        ifaceIndex=interface.ifaceIndex,
                        pvid=is_pvid,
                    )
                    complete_interface_list.append(response_dict)
                    break

        return complete_interface_list

    def get_interface_vlans(self, interface_id):
        config_query = AvlanConfigQuery(self._dao)
        vlans_on_interface = config_query.get_interface_vlans(
            ifaceId=interface_id,
        )

        '''
        TODO: resolve this by join in db
        TODO: pass nodeId to reduce amount of results
        '''
        complete_vlan_list = []
        vlans = config_query.get_vlans()
        for vlan_on_interface in vlans_on_interface:
            for vlan in vlans:
                if vlan_on_interface.vlanId == vlan.id:
                    if vlan_on_interface.pvid == 1:
                        is_pvid = 'True'
                    else:
                        is_pvid = ''
                    response_dict = dict(
                        number=vlan.number,
                        name=vlan.name,
                        is_pvid=is_pvid,
                    )
                    complete_vlan_list.append(response_dict)
                    break

        return complete_vlan_list

    def get_nodes(self):
        node_list = []
        config_query = AvlanConfigQuery(self._dao)
        nodes = config_query.get_nodes()

        for node in nodes:
            node_dict = dict(
                id=node.id,
                title=node.ipAddress,
                label=node.name,
            )
            node_dict['vlan'] = []
            interfaces = config_query.get_interfaces(nodeId=node.id)
            for interface in interfaces:
                interface_vlans = config_query.get_interface_vlans(
                    ifaceId=interface.id
                )
                for interface_vlan in interface_vlans:
                    vlans = config_query.get_vlans(id=interface_vlan.vlanId)
                    if len(vlans) > 0:
                        vlan = vlans[0]
                        node_dict['vlan'].append(vlan.number)
            node_list.append(node_dict)
        return node_list

    def get_node_available_interfaces(self, node_id):
        config_query = AvlanConfigQuery(self._dao)
        node_interfaces = config_query.get_interfaces(
            nodeId=node_id,
        )

        # Filter out interfaces with connections
        available_interfaces = []
        for node_interfaces in node_interfaces:
            # maybe null...
            peer_node_id = node_interfaces.peerNodeId
            if peer_node_id is None or peer_node_id == 0:
                available_interfaces.append(node_interfaces)

        return available_interfaces

    def get_vlans(self):
        vlan_list = []
        config_query = AvlanConfigQuery(self._dao)
        vlans = config_query.get_vlans()
        for vlan in vlans:
            vlan_list.append(vlan.number)
        vlan_list = list(set(vlan_list))
        return vlan_list

    def get_edges(self):
        edges_list = []
        config_query = AvlanConfigQuery(self._dao)
        interfaces = config_query.get_interfaces()
        added_edges = []
        nodes = config_query.get_nodes()
        interface_vlans = config_query.get_interface_vlans()
        vlans = config_query.get_vlans()

        for interface in interfaces:
            if interface.peerNodeId is None or interface.id in added_edges:
                continue

            for peer_interface in interfaces:
                if interface.peerIfaceId == peer_interface.id:
                    break

            interface_node = None
            peer_interface_node = None
            for node in nodes:
                if interface.nodeId == node.id:
                    interface_node = node
                elif peer_interface.nodeId == node.id:
                    peer_interface_node = node
                if (
                    interface_node is not None and
                    peer_interface_node is not None
                ):
                    break

            label = "{0:s}({1:s}) - {2:s}({3:s})".format(
                interface_node.name,
                str(interface.ifaceIndex),
                peer_interface_node.name,
                str(peer_interface.ifaceIndex),
            )

            title = "Connecting: {0:s} ({1:s}) and {2:s} ({3:s})".format(
                interface_node.name,
                str(interface.ifaceIndex),
                peer_interface_node.name,
                str(peer_interface.ifaceIndex),
            )
            edge_dict = {
                'from': interface.nodeId,
                'to': interface.peerNodeId,
                'label': label,
                'title': title
            }
            added_edges.append(interface.id)
            added_edges.append(peer_interface.id)
            edges_list.append(edge_dict)

            edge_dict['vlan'] = {}

            for interface_vlan in interface_vlans:
                if (
                    interface_vlan.ifaceId != interface.id and
                    interface_vlan.ifaceId != interface.peerIfaceId
                ):
                    continue

                for vlan in vlans:
                    if vlan.id != interface_vlan.vlanId:
                        continue

                    vlan_number = vlan.number

                    if vlan_number not in edge_dict['vlan']:
                        edge_dict['vlan'][vlan_number] = 'none'

                    if (
                        interface_vlan.ifaceId == interface.id and
                        interface_vlan.pvid
                    ):
                        if edge_dict['vlan'][vlan_number] == 'none':
                            edge_dict['vlan'][vlan_number] = 'from'
                        else:
                            edge_dict['vlan'][vlan_number] = 'both'
                    elif (
                        interface_vlan.ifaceId == interface.peerIfaceId and
                        interface_vlan.pvid
                    ):
                        if edge_dict['vlan'][vlan_number] == 'none':
                            edge_dict['vlan'][vlan_number] = 'to'
                        else:
                            edge_dict['vlan'][vlan_number] = 'both'
        return edges_list
