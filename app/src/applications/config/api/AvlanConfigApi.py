from cgi import FieldStorage
from json import (
    dump,
    load
)
from shutil import copyfileobj

from jsonschema import (
    validate,
    ValidationError,
)
from os import (
    makedirs,
    remove,
)
from os.path import (
    abspath as path_abspath,
    basename as path_basename,
    join as path_join,
    exists as path_exists,
)

from src.applications.base.api.AvlanBaseApi import (
    AvlanBaseApi,
    AvlanApiException,
)
from src.applications.config.query.AvlanConfigQuery import AvlanConfigQuery
from src.applications.config.storage.AvlanConfigStorage import \
    AvlanConfigStorage
from src.utils.crawler.AvlanCrawler import AvlanCrawler


class AvlanConfigApi(AvlanBaseApi):
    def list_configs(self):
        example_config = AvlanConfigStorage()
        configs = self._dao.list(example_config)
        return configs

    def run_config(self, id, result_list):
        config_query = AvlanConfigQuery(self._dao)
        config = config_query.get_config(
            id=id,
        )

        '''
        TODO: set config directory from settings
        '''
        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        config_file = path_join(
            config_directory,
            '{0}.json'.format(config.title),
        )

        crawler = AvlanCrawler(
            input_file=config_file,
            messenger=self._redis,
        )

        '''
        Catch and log all exceptions both to GUI and console as this method
        is meant to be run as sub-thread, stopping activity indicator and
        displaying error message (if any). Communication between threads is
        handled via mutable object passed via reference (result list).
        '''
        try:
            crawler.crawl()
            crawler.write_config(config_file)
        except Exception, e:
            result_list.append(e.message)
            raise

        self.load_config(id, result_list)

    def load_config(self, id, result_list):
        config_query = AvlanConfigQuery(self._dao)
        config = config_query.get_config(
            id=id,
        )
        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        config_file = path_join(
            config_directory,
            '{0}.json'.format(config.title),
        )

        try:
            with open(config_file) as e:
                config_dict = load(e)
                self.validate_json(config_dict)
        except Exception, e:
                result_list.append(e.message)
                raise
        '''
        TODO: setup should be stored in database per user basis
        '''

        try:
            config_query.remove_nodes()
            config_query.remove_interfaces()
            config_query.remove_vlans()
        except Exception, e:
            result_list.append(e.message)
            raise

        vlan_dict = {}

        '''
        We are sure that everything, that was required is set up.
        TODO: use json schema - to class mapper
        '''

        schema_file = path_join(
            'resources',
            'schema.json',
        )
        with open(schema_file) as s:
            schema_json = load(s)

        node_schema = schema_json['properties']['nodes']['items']['properties']
        interface_schema = node_schema["interfaces"]["items"]["properties"]
        vlan_schema = interface_schema["vlans"]["items"]["properties"]

        for node in config_dict['nodes']:
            node_id = node['id']
            vlan_dict[node_id] = {}
            node_kwargs = {}

            for field, field_details in node_schema.iteritems():
                if field_details['type'] == 'array':
                    continue
                try:
                    node_kwargs[field] = node[field]
                except KeyError:
                    if "default" in field_details:
                        node_kwargs[field] = field_details["default"]
                    else:
                        node_kwargs[field] = None

            try:
                config_query.create_node(**node_kwargs)
            except Exception, e:
                result_list.append(e.message)
                raise

            try:
                for interface in node['interfaces']:
                    interface_kwargs = {}
                    for field, field_details in interface_schema.iteritems():
                        if field_details['type'] == 'array':
                            continue
                        try:
                            interface_kwargs[field] = interface[field]
                        except KeyError:
                            if "default" in field_details:
                                interface_kwargs[field] = field_details[
                                    "default"
                                ]
                            else:
                                interface_kwargs[field] = None

                    interface_kwargs['nodeId'] = node_id

                    interface_id = interface['id']

                    try:
                        config_query.create_interface(**interface_kwargs)
                    except Exception, e:
                        result_list.append(e.message)
                        raise

                    try:
                        for vlan in interface['vlans']:
                            vlan_kwargs = {}
                            for field, field_details in vlan_schema.iteritems():
                                try:
                                    vlan_kwargs[field] = vlan[field]
                                except KeyError:
                                    vlan_kwargs[field] = None

                            vlan_number = str(vlan_kwargs['number'])
                            vlan_name = vlan_kwargs['name']
                            is_pvid = vlan_kwargs['pvid']

                            if vlan_number not in vlan_dict[node_id]:
                                vlan_dict[node_id][vlan_number] = {}
                                vlan_dict[node_id][vlan_number]['name'] = vlan_name
                                vlan_dict[node_id][vlan_number]['node'] = node_id
                                vlan_dict[node_id][vlan_number]['interfaces'] = []

                            vlan_dict[node_id][vlan_number]['interfaces'].append(
                                {
                                    'ifaceId': interface_id,
                                    'pvid': is_pvid,
                                }
                            )
                    except KeyError:
                        continue

            except KeyError:
                continue

        for vlans_on_node in vlan_dict.itervalues():
            for vlan_number, vlan_details in vlans_on_node.iteritems():
                try:
                    vlan = config_query.create_vlan(
                        vlan_number,
                        vlan_details['node'],
                        vlan_details['name'],
                    )
                except Exception, e:
                    result_list.append(e.message)
                    raise

                try:
                    for interface_details in vlan_details['interfaces']:
                        config_query.create_interface_vlan(
                            ifaceId=interface_details['ifaceId'],
                            vlanId=vlan.id,
                            pvid=interface_details['pvid'],
                        )
                except Exception, e:
                    result_list.append(e.message)
                    raise

        active_config = config_query.get_config(
            active=1
        )
        if active_config is not None:
            active_config.active = 0
            self._dao.update(active_config)

        config.active = 1
        self._dao.update(config)

    @staticmethod
    def validate_json(json):
        schema_file = path_join(
            'resources',
            'schema.json',
        )
        try:
            with open(schema_file) as s:
                schema_json = load(s)

            validate(
                    json,
                    schema_json,
            )
        except ValidationError, e:
            raise AvlanApiException(e)

    def create_config(self, payload):
        config_query = AvlanConfigQuery(self._dao)

        if 'title' not in payload:
            raise AvlanApiException("Parameters cannot be empty!")
        title = payload['title']

        try:
            created_config = config_query.create_config(
                title=title,
            )

        #TODO, find which exception to catch
        except:
            raise AvlanApiException(
                'Failed to create config {0:s}'.format(title)
            )

        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        if not path_exists(config_directory):
            makedirs(config_directory)

        config_file = path_join(
            config_directory,
            '{0:s}.json'.format(title),
        )

        config_file_handle = open(
            config_file,
            'wb'
        )

        if (
            'config' in payload and
            isinstance(
                payload['config'],
                FieldStorage,
            )
        ):
            config_payload = payload['config']
            copyfileobj(
                config_payload.file,
                config_file_handle,
                100000,
            )
            config_file_handle.close()

            try:
                with open(config_file) as config:
                    config_json = load(config)
                    self.validate_json(config_json)
            except ValueError:
                remove(config_file)
                raise AvlanApiException("Invalid input!")
        else:
            '''
            Write empty config
            '''
            config_file_handle.write(
                '{"nodes": []}'
            )
            config_file_handle.close()

        active_config = config_query.get_config(
            active=1
        )
        if active_config is not None:
            active_config.active = 0
            self._dao.update(active_config)

        created_config.active = 1
        self._dao.update(created_config)

    def get_config(self, id):
        config_query = AvlanConfigQuery(self._dao)
        config = config_query.get_config(
            id=id,
        )
        return config

    def get_config_path(self, id):
        config = self.get_config(id)
        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        config_file = path_join(
            config_directory,
            '{0}.json'.format(config.title),
        )

        return {
            'path': config_file,
            'filename': path_basename(config_file),
        }

    def delete_config(self, id):
        config_query = AvlanConfigQuery(self._dao)
        config = config_query.get_config(
            id=id,
        )

        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        config_file = path_join(
            config_directory,
            '{0}.json'.format(config.title),
        )

        remove(config_file)
        self._dao.delete(config)

    def create_node(self, payload, result_list):
        '''
        TODO: add payload validation.
        '''
        config_query = AvlanConfigQuery(self._dao)
        configs = self.list_configs()

        active_config = None
        for config in configs:
            if config.active == 1:
                active_config = config
                break

        try:
            new_node = {
                'name': payload['name'],
                'type': payload['type'],
                'ipAddress': payload['ip'],
                'sshPort': int(payload['ssh_port']),
                'sshUsername': payload['ssh_username'],
                'sshPassword': payload['ssh_password'],
            }
        except KeyError, e:
            result_list.append(e.message)
            raise

        try:
            config_query.create_node(**new_node)
        except Exception, e:
            result_list.append(e.message)
            raise

        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        config_file = path_join(
            config_directory,
            '{0}.json'.format(active_config.title),
        )

        config_file_handle = open(
            config_file,
            'r+',
        )

        config_json = load(config_file_handle)

        '''
        Find first available id
        '''
        max_id = 0
        for test_node in config_json['nodes']:
            test_node_id = test_node['id']
            if test_node_id > max_id:
                max_id = test_node_id
        max_id += 1

        new_node['id'] = max_id
        new_node['interfaces'] = []

        config_json['nodes'].append(new_node)

        config_file_handle.seek(0)

        dump(
            obj=config_json,
            fp=config_file_handle,
            indent=4,
        )

        config_file_handle.truncate()
        config_file_handle.close()

    def create_edge(self, payload, result_list):
        '''
        TODO: add payload validation.
        '''
        config_query = AvlanConfigQuery(self._dao)
        configs = self.list_configs()

        active_config = None
        for config in configs:
            if config.active == 1:
                active_config = config
                break

        # lame validation
        try:
            node_a_id = int(payload['source_node_id'])
            interface_a_id = int(payload['source_interface_id'])
            node_b_id = int(payload['target_node_id'])
            interface_b_id = int(payload['target_interface_id'])
        except Exception, e:
            result_list.append(e.message)
            raise

        '''
        Write to db. Source node first, then target node.
        '''
        try:
            interface_a = config_query.get_interfaces(id=interface_a_id)[0]
            interface_b = config_query.get_interfaces(id=interface_b_id)[0]

            interface_a.peerNodeId = node_b_id
            interface_a.peerIfaceId = interface_b_id
            self._dao.update(interface_a)

            interface_b.peerNodeId = node_a_id
            interface_b.peerIfaceId = interface_a_id
            self._dao.update(interface_b)
        except Exception, e:
            result_list.append(e.message)
            raise

        '''
        Write to active config.
        '''
        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        config_file = path_join(
            config_directory,
            '{0}.json'.format(active_config.title),
        )

        config_file_handle = open(
            config_file,
            'r+',
        )

        config_json = load(config_file_handle)

        for test_node in config_json['nodes']:
            test_node_id = test_node['id']
            if test_node_id == node_a_id:
                for node_a_interface in test_node['interfaces']:
                    if node_a_interface['id'] == interface_a_id:
                        node_a_interface['peerNodeId'] = node_b_id
                        node_a_interface['peerIfaceId'] = interface_b_id
            elif test_node_id == node_b_id:
                for node_b_interface in test_node['interfaces']:
                    if node_b_interface['id'] == interface_b_id:
                        node_b_interface['peerNodeId'] = node_a_id
                        node_b_interface['peerIfaceId'] = interface_a_id

        config_file_handle.seek(0)

        dump(
            obj=config_json,
            fp=config_file_handle,
            indent=4,
        )

        config_file_handle.truncate()
        config_file_handle.close()

    def delete_edge(self, payload, result_list):
        '''
        TODO: add payload validation.
        '''
        config_query = AvlanConfigQuery(self._dao)
        configs = self.list_configs()

        active_config = None
        for config in configs:
            if config.active == 1:
                active_config = config
                break

        # lame validation
        try:
            node_a_id = int(payload['source_node_id'])
            interface_a_id = int(payload['source_interface_id'])
            node_b_id = int(payload['target_node_id'])
            interface_b_id = int(payload['target_interface_id'])
        except Exception, e:
            result_list.append(e.message)
            raise

        '''
        Write to db. Source node first, then target node.
        '''
        try:
            interface_a = config_query.get_interfaces(id=interface_a_id)[0]
            interface_b = config_query.get_interfaces(id=interface_b_id)[0]

            interface_a.peerNodeId = None
            interface_a.peerIfaceId = None
            self._dao.update(
                interface_a,
                ignore_none=False,
            )

            interface_b.peerNodeId = None
            interface_b.peerIfaceId = None
            self._dao.update(
                interface_b,
                ignore_none=False,
            )
        except Exception, e:
            result_list.append(e.message)
            raise

        '''
        Write to active config.
        '''
        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        config_file = path_join(
            config_directory,
            '{0}.json'.format(active_config.title),
        )

        config_file_handle = open(
            config_file,
            'r+',
        )

        config_json = load(config_file_handle)

        for test_node in config_json['nodes']:
            test_node_id = test_node['id']
            if test_node_id == node_a_id:
                for node_a_interface in test_node['interfaces']:
                    if node_a_interface['id'] == interface_a_id:
                        node_a_interface.pop('peerNodeId')
                        node_a_interface.pop('peerIfaceId')

            elif test_node_id == node_b_id:
                for node_b_interface in test_node['interfaces']:
                    if node_b_interface['id'] == interface_b_id:
                        node_b_interface.pop('peerNodeId')
                        node_b_interface.pop('peerIfaceId')

        config_file_handle.seek(0)

        dump(
            obj=config_json,
            fp=config_file_handle,
            indent=4,
        )

        config_file_handle.truncate()
        config_file_handle.close()

    def delete_node(self, payload, result_list):
        '''
        TODO: add payload validation.
        '''
        config_query = AvlanConfigQuery(self._dao)
        configs = self.list_configs()

        active_config = None
        for config in configs:
            if config.active == 1:
                active_config = config
                break

        # lame validation
        try:
            node_id = int(payload['node_id'])
        except Exception, e:
            result_list.append(e.message)
            raise

        '''
        Write to db. Source node first, then target node.
        '''
        try:
            node = config_query.get_nodes(id=node_id)[0]
            node_interfaces = config_query.get_interfaces(
                nodeId=node_id
            )

            # Detach connections
            peer_interfaces = config_query.get_interfaces(
                peerNodeId=node_id,
            )

            for peer_interface in peer_interfaces:
                peer_interface.peerIfaceId = None
                peer_interface.peerNodeId = None
                self._dao.update(
                    peer_interface,
                    ignore_none=False,
                )

            vlans_on_node = config_query.get_vlans(
                nodeId=node_id
            )

            for vlan_on_node in vlans_on_node:
                self._dao.delete(vlan_on_node)

            for node_interface in node_interfaces:
                self._dao.delete(node_interface)

            self._dao.delete(node)
        except Exception, e:
            result_list.append(e.message)
            raise

        '''
        Write to active config.
        '''
        config_directory = path_abspath(
            path_join(
                'storage',
                'config',
            )
        )

        config_file = path_join(
            config_directory,
            '{0}.json'.format(active_config.title),
        )

        config_file_handle = open(
            config_file,
            'r+',
        )

        config_json = load(config_file_handle)

        node_index_in_json = None
        step = 0
        for test_node in config_json['nodes']:
            if test_node['id'] == node_id and node_index_in_json is None:
                node_index_in_json = step
            else:
                step += 1

            if 'interfaces' not in test_node:
                continue

            for interface in test_node['interfaces']:
                if 'peerNodeId' not in interface:
                    continue
                if interface['peerNodeId'] == node_id:
                    interface.pop('peerNodeId')
                    interface.pop('peerIfaceId')

        if node_index_in_json is None:
            raise AvlanApiException

        del config_json['nodes'][node_index_in_json]
        config_file_handle.seek(0)

        dump(
            obj=config_json,
            fp=config_file_handle,
            indent=4,
        )

        config_file_handle.truncate()
        config_file_handle.close()
