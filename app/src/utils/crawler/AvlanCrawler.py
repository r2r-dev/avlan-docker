from json import (
    load,
    dump,
    dumps,
)

from jsonschema import validate

from src.utils.crawler.mediator.AvlanCrawlerMediatorFactory import \
    AvlanCrawlerMediatorFactory


class AvlanCrawler(object):
    def __init__(self, input_file, schema_file=None, messenger=None):
        self.__messenger = messenger
        self.__mediators = []

        with open(input_file) as input_file_handler:
            self.__input = load(input_file_handler)

        if schema_file is not None:
            with open(schema_file) as s:
                schema_json = load(s)

            validate(
                self.__input,
                schema_json,
            )

        for input_node in self.__input['nodes']:
            mediator = AvlanCrawlerMediatorFactory.factory(
                type=input_node['type'],
                node=input_node,
                messenger=messenger,
            )
            self.__mediators.append(mediator)

    def get_config(self):
        return dumps(
            obj=self.__input,
        )

    def write_config(self, output_location):
        with open(
            name=output_location,
            mode='w',
        ) as output_file:
            dump(
                obj=self.__input,
                fp=output_file,
                indent=2,
            )

    def crawl(self):
        for mediator in self.__mediators:
            mediator.fetch_remote_data()
        self.__fill_interface_ids()
        self.__discover_connections()

        if self.__messenger:
            self.__messenger.set('command', '')
            self.__messenger.set('output', '')
            self.__messenger.set('ip', '')
            self.__messenger.set('name', '')

    def __discover_connections(self):
        def merge_output(x, y):
            z = x.copy()
            z.update(y)
            return z

        mac_address_map = {}

        for mediator in self.__mediators:
            mac_address_map = merge_output(
                mac_address_map,
                mediator.get_lldp_neighbors(),
            )

        for iface_a_mac, iface_b_mac in mac_address_map.iteritems():
            node_a = None
            node_a_interface = None

            node_b = None
            node_b_interface = None

            both_nodes_and_interfaces_found = False
            for node in self.__input['nodes']:
                interface_found = False
                for interface in node['interfaces']:
                    if interface['mac'] == iface_a_mac:
                        node_a_interface = interface
                        node_a = node
                        interface_found = True
                    elif interface['mac'] == iface_b_mac:
                        node_b_interface = interface
                        node_b = node
                        interface_found = True
                    if interface_found:
                        break

                both_nodes_and_interfaces_found = (
                    node_a is not None
                    and
                    node_a_interface is not None
                    and
                    node_b is not None
                    and
                    node_b_interface is not None
                )
                if both_nodes_and_interfaces_found:
                    break

            if both_nodes_and_interfaces_found:
                node_a_interface['peerNodeId'] = node_b['id']
                node_a_interface['peerIfaceId'] = node_b_interface['id']

                node_b_interface['peerNodeId'] = node_a['id']
                node_b_interface['peerIfaceId'] = node_a_interface['id']

    def __fill_interface_ids(self):
        '''
        Assign unique ids to new interfaces
        '''

        max_id = 0
        for node in self.__input['nodes']:
            if 'interfaces' not in node:
                continue
            for interface in node['interfaces']:
                if 'id' not in interface:
                    continue
                interface_id = interface['id']
                if interface['id'] > max_id:
                    max_id = interface_id

        for node in self.__input['nodes']:
            if 'interfaces' not in node:
                continue
            for interface in node['interfaces']:
                if 'id' not in interface:
                    max_id += 1
                    interface['id'] = max_id
