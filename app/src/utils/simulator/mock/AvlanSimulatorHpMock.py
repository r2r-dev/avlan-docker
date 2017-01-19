from MockSSH import SSHCommand

from src.utils.simulator.mock.AvlanSimulatorBaseMock import\
    AvlanSimulatorBaseMock

from src.utils.simulator.generator.AvlanSimulatorBaseCommandGenerator import \
    AvlanSimulatorBaseCommandGenerator


class ShowLLDPInfoRemoteDevicePortGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, connections):
        super(
            ShowLLDPInfoRemoteDevicePortGenerator,
            self
        ).__init__()
        self.__connections = connections

    def _generate(self):
        outputs = {}
        for interface, remote_mac in self.__connections.iteritems():
            normalized_mac = remote_mac.replace(
                ":",
                " ",
            ).lower()

            outputs[interface] = [
                '',
                ' LLDP Remote Device Information Detail',
                '',
                '  Local Port   : {0:}'.format(interface),
                '  ChassisType  : mac-address',
                '  ChassisId    : {0:s}'.format(normalized_mac),
                '  PortType     : mac-...',
                '  PortId       : {0:s}'.format(normalized_mac),
                '  SysName      : simulator',
                '  System Descr : simulator',
                '  PortDescr    : simulator',
                '',
                '',
                '  System Capabilities Supported  : router',
                '  System Capabilities Enabled    : router',
                '',
                '  Remote Management Address',
                '     Type    : ipv4',
                '     Address : 0.0.0.0',
                '',
                '',
            ]
        return outputs


class ShowLLDPInfoRemoteDeviceGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, connections):
        super(
            ShowLLDPInfoRemoteDeviceGenerator,
            self
        ).__init__()
        self.__connections = connections

    def _generate(self):
        output = [
            '',
            ' LLDP Remote Devices Information',
            '',
            '  LocalPort | ChassisId                 PortId PortDescr SysName ',
            '  --------- + ------------------------- ------ ---------'
            ' ----------------------',
        ]

        port_template = '  {:<9} | {:<25} {:<6} {:<9} {:<22}'

        for key, remote_mac in self.__connections.iteritems():
            normalized_mac = remote_mac.replace(
                ":",
                " ",
            ).lower()

            output += [
                port_template.format(
                    key,
                    normalized_mac,
                    "{0:s} ...".format(
                        normalized_mac[:2]
                    ),
                    "simulator",
                    "simulator",
                )
            ]

        output += (
            '',
            '',
        )

        return output


class ShowLLDPInfoLocalDeviceGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, interfaces):
        super(
            ShowLLDPInfoLocalDeviceGenerator,
            self
        ).__init__()
        self.__interfaces = interfaces

    def _generate(self):
        output = [
            '',
            ' LLDP Local Device Information',
            '',
            '  Chassis Type : mac-address',
            '  Chassis Id   : 00 00 00 00 00 00',
            '  System Name  : simulator',
            '  System Description : HP',
            '  System Capabilities Supported:bridge, router',
            '  System Capabilities Enabled:bridge',
            '',
            '  Management Address  :',
            '     Type:ipv4',
            '     Address:0.0.0.0',
            '',
            ' LLDP Port Information',
            '',
            '  Port     | PortType PortId   PortDesc',
            '  -------- + -------- -------- --------',
        ]

        port_template = '  {:<8} | local    {:<8} {:<8}'
        step = 1
        for interface in self.__interfaces:
            iface_index = interface['ifaceIndex']
            output += [
                port_template.format(
                    iface_index,
                    step,
                    iface_index,
                )
            ]
            step += 1

        return output


class ShowVlansPortGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, interfaces):
        super(
            ShowVlansPortGenerator,
            self
        ).__init__()
        self.__interfaces = interfaces

    def _generate(self):
        outputs = {}
        for interface in self.__interfaces:
            port = interface['ifaceIndex']
            output = []
            output += (
                '',
                ' Status and Counters - VLAN Information -'
                ' for ports {0:s}'.format(port),
                '',
                '  VLAN ID Name                             |'
                ' Status     Voice Jumbo',
                '  ------- -------------------------------- +'
                ' ---------- ----- -----',
            )
            if 'vlans' in interface:
                vlan_template = '  {:<7} {:<32} | Port-based No    No'
                output = reduce(
                    lambda old, new: old + [
                        vlan_template.format(
                            new['number'],
                            new['name'],
                        )
                    ],
                    interface['vlans'],
                    output,
                )
            output += (
                '',
                '',
            )
            outputs[port] = output
        return outputs


class ShowVlansGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, vlans):
        super(
            ShowVlansGenerator,
            self
        ).__init__()
        self.__vlans = vlans

    def _generate(self):
        '''
        Generate output for "show vlans" command.
        '''
        output = [
            '',
            ' Status and Counters - VLAN Information',
            '',
        ]
        output += (
            '  Maximum VLANs to support : {0:d}'.format(
                len(self.__vlans)
            ),
        )

        '''
        TODO: default vlan number should be provided here
        '''
        output += (
            '  Primary VLAN : {0:d}'.format(1),
        )
        output += (
            '  Management VLAN :',
            '',
            '  VLAN ID Name                             | Status     Voice '
            'Jumbo',
            '  ------- -------------------------------- + ---------- ----- '
            '-----',
        )
        vlan_template = '  {:<7} {:<32} | Port-based No    No'
        output = reduce(
            lambda old, new: old + [
                vlan_template.format(
                    new['number'],
                    new['name'],
                )
            ],
            self.__vlans.values(),
            output,
        )
        output += (
            '',
            '',
        )
        return output


class ShowInterfacesStatusGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, interfaces):
        super(
            ShowInterfacesStatusGenerator,
            self
        ).__init__()
        self.__interfaces = interfaces

    def _generate(self):
        def __find_pvid(interface):
            if 'vlans' in interface:
                for vlan in interface['vlans']:
                    if 'pvid' in vlan and vlan['pvid'] is True:
                        return vlan['number']

            '''
            TODO: default vlan should be extracted and returned here
            '''
            return 1

        output = [
            '  Port     Name       Status  Config-mode   Speed    Type       '
            'Tagged Untagged',
            '  -------- ---------- ------- ------------- -------- ---------- '
            '------ --------',
        ]
        interface_template = '  {:<8} {:<10} Up      Auto          100FDx' \
                             '   100/1000T  multi  {:<8}'

        output = reduce(
            lambda old, new: old + [
                interface_template.format(
                    new['ifaceIndex'],
                    '',
                    __find_pvid(new),
                )
            ],
            self.__interfaces,
            output,
        )
        return output


class ShowInterfacesAllGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, interfaces):
        super(
            ShowInterfacesAllGenerator,
            self
        ).__init__()
        self.__interfaces = interfaces

    @staticmethod
    def _generate_single_interface_output(interface):
        output = [
            ' Status and Counters - Port Counters for port {0:}'.format(
                interface['ifaceIndex'],
            ),
            '',
            '  Name  :',
            '  MAC Address      : {0:s}'.format(interface['mac'])
        ]

        output += [
            '  Link Status      : Down',
            '  Totals (Since boot or last clear) :',
            '   Bytes Rx        : 0                  Bytes Tx        : 0',
            '   Unicast Rx      : 0                  Unicast Tx      : 0',
            '   Bcast/Mcast Rx  : 0                  Bcast/Mcast Tx  : 0',
            '  Errors (Since boot or last clear) :',
            '   FCS Rx          : 0                  Drops Tx        : 0',
            '   Alignment Rx    : 0                  Collisions Tx   : 0',
            '   Runts Rx        : 0                  Late Colln Tx   : 0',
            '   Giants Rx       : 0                  Excessive Colln : 0',
            '   Total Rx Errors : 0                  Deferred Tx     : 0',
            '  Others (Since boot or last clear) :',
            '   Discard Rx      : 0                  Out Queue Len   : 0',
            '   Unknown Protos  : 0',
            '  Rates (5 minute weighted average) :',
            '   Total Rx  (bps) : 0         		Total Tx  (bps) : 0',
            '   Unicast Rx (Pkts/sec) : 0         	Unicast Tx (Pkts/sec) : 0',
            '   B/Mcast Rx (Pkts/sec) : 0         	B/Mcast Tx (Pkts/sec) : 0',
            '   Utilization Rx  :     0 %		Utilization Tx  :     0 %',
            '',
            '',
        ]

        return output

    def _generate(self):
        output = ['']
        for interface in self.__interfaces:
            output += self._generate_single_interface_output(interface)

        return output


class AvlanSimulatorHpMock(AvlanSimulatorBaseMock):
    def __init__(self, config):
        super(
            AvlanSimulatorHpMock,
            self
        ).__init__(
            config=config,
        )

        self._command_output_mapping = {
            'show_vlans': ShowVlansGenerator(
                vlans=self._vlans,
            ),
            'show_interfaces_status': ShowInterfacesStatusGenerator(
                interfaces=self._interfaces,
            ),
            'show_interfaces_all': ShowInterfacesAllGenerator(
                interfaces=self._interfaces,
            ),
            'show_vlans_port': ShowVlansPortGenerator(
                interfaces=self._interfaces,
            ),
            'show_lldp_info_local_device': ShowLLDPInfoLocalDeviceGenerator(
                interfaces=self._interfaces,
            ),
            'show_lldp_info_remote_device': ShowLLDPInfoRemoteDeviceGenerator(
                connections=self._connection_map,
            ),
            'show_lldp_info_remote_device_port':
                ShowLLDPInfoRemoteDevicePortGenerator(
                    connections=self._connection_map,
                ),
        }

        self._construct_commands()

    def _construct_commands(self):
        '''
        Generate command classes for a mock using pre-generated outputs.
        '''

        command_output_mapping = self._command_output_mapping
        connection_map = self._connection_map

        class CommandShow(SSHCommand):
            name = 'show'

            def start(self):
                help_msg = (
                    "MockSSH: Supported usage: ",
                    "show vlans",
                    "show vlans port <port-number>",
                    "show interfaces status",
                    "show interfaces all",
                    "show lldp info local-device",
                    "show lldp info remote-device",
                    "show lldp info remote-device <port>",
                    "",
                    "vlan available ports: {0:s}".format(
                        reduce(
                            lambda old, new: "{0:s}, {1:s}".format(
                                str(old),
                                str(new),
                            ),
                            command_output_mapping[
                                'show_vlans_port'
                            ].output.keys()
                        )
                    ),
                    "lldp info remote-device ports: {0:s}".format(
                        reduce(
                            lambda old, new: "{0:s}, {1:s}".format(
                                str(old),
                                str(new),
                            ),
                            connection_map.keys(),
                            ''
                        )
                    ),
                )

                arguments_count = len(self.args)
                is_show_vlans = (
                    arguments_count == 1
                    and self.args[0] == 'vlans'
                )
                is_show_interfaces_status = (
                    arguments_count == 2
                    and ' '.join(self.args) == 'interfaces status'
                )
                is_show_interfaces_all = (
                    arguments_count == 2
                    and ' '.join(self.args) == 'interfaces all'
                )
                is_show_vlans_port = (
                    arguments_count == 3
                    and ' '.join(self.args[:-1]) == 'vlans port'
                    and self.args[-1] in command_output_mapping[
                        'show_vlans_port'
                    ].output.keys()
                )
                is_show_lldp_info_local_device = (
                    arguments_count == 3
                    and ' '.join(self.args) == 'lldp info local-device'
                )
                is_show_lldp_info_remote_device = (
                    arguments_count == 3
                    and ' '.join(self.args) == 'lldp info remote-device'
                )
                is_show_lldp_info_remote_device_port = (
                    arguments_count == 4
                    and ' '.join(self.args[:-1]) == 'lldp info remote-device'
                    and self.args[-1] in connection_map.keys()
                )
                if is_show_vlans:
                    output = command_output_mapping['show_vlans'].output
                elif is_show_interfaces_status:
                    output = command_output_mapping[
                        'show_interfaces_status'
                    ].output
                elif is_show_interfaces_all:
                    output = command_output_mapping[
                        'show_interfaces_all'
                    ].output
                elif is_show_lldp_info_local_device:
                    output = command_output_mapping[
                        'show_lldp_info_local_device'
                    ].output
                elif is_show_lldp_info_remote_device:
                    output = command_output_mapping[
                        'show_lldp_info_remote_device'
                    ].output
                elif is_show_lldp_info_remote_device_port:
                    try:
                        output = command_output_mapping[
                            'show_lldp_info_remote_device_port'
                        ].output[self.args[-1]]
                    except KeyError:
                        output = help_msg
                elif is_show_vlans_port:
                    try:
                        output = command_output_mapping[
                            'show_vlans_port'
                        ].output[self.args[-1]]
                    except KeyError:
                        output = help_msg
                else:
                    output = help_msg

                for line in output:
                    self.writeln(line)
                self.exit()
        self._commands.append(CommandShow)
