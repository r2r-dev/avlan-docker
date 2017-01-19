from abc import (
    ABCMeta,
    abstractmethod,
)

from MockSSH import runServer


class AvlanSimulatorBaseMock(object):
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self._name = config['name']
        self._ip = config['ipAddress']
        self._port = int(config['sshPort'])
        self._username = config['sshUsername']
        self._password = config['sshPassword']
        self._interfaces = config['interfaces']
        self._connection_map = config['connection_map']
        self._commands = []
        self._vlans = {}

        self.__extract_vlans()

    @abstractmethod
    def _construct_commands(self):
        pass

    def execute(self):
        runServer(
            self._commands,
            prompt="{}#".format(self._name),
            interface=self._ip,
            port=self._port,
            **{self._username: self._password}
        )

    def __extract_vlans(self):
        '''
        Extract list of vlans together with interfaces
        '''
        vlans = {}

        for interface in self._interfaces:
            if 'vlans' not in interface:
                continue

            for vlan in interface['vlans']:
                vlan_name = vlan['name']
                vlan_id = vlan['number']

                if vlan_id not in vlans:
                    vlans[vlan_id] = {
                        'number': vlan_id,
                        'name': vlan_name,
                        'ports': [],
                    }

                vlans[vlan_id]['ports'].append(interface['ifaceIndex'])

        self._vlans = vlans
