from MockSSH import SSHCommand

from src.utils.simulator.mock.AvlanSimulatorBaseMock import\
    AvlanSimulatorBaseMock

from src.utils.simulator.generator.AvlanSimulatorBaseCommandGenerator import \
    AvlanSimulatorBaseCommandGenerator


class ShowLLDPInfoRemoteDetailGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, connections):
        super(
            ShowLLDPInfoRemoteDetailGenerator,
            self
        ).__init__()
        self.__connections = connections

    def _generate(self):
        outputs = {}
        for interface, remote_mac in self.__connections.iteritems():
            normalized_mac = remote_mac.replace(
                ":",
                "-",
            )

            outputs[interface] = [
                'LLDP Remote Devices Information Detail',
                '--------------------------------------------------------------'
                '----------------',
                ' Index                : 0',
                ' Chassis Type         : MAC Address',
                ' Chassis ID           : 00-00-00-00-00-00',
                ' Port ID Type         : MAC Address',
                ' Port ID              : {0:s}'.format(normalized_mac),
                ' Time To Live         : 0 seconds',
                ' Port Description     : simulator',
                ' System Name          : simulator',
                ' System Description   : simulator',
                ' System Capabilities  : Bridge',
                ' Enabled Capabilities : Bridge',
                '',
                ' Management Address : 0.0.0.0 (IPv4)',
                '',
                ' Port VLAN ID : 1',
                '',
                ' Port and Protocol VLAN ID : supported, disabled',
                ' VLAN Name : VLAN    1 - Default',
                '',
                ' Protocol Identity (Hex) : 88-CC',
                '',
                ' MAC/PHY Configuration/Status',
                '  Port Auto-neg Supported            : Yes',
                '  Port Auto-neg Enabled              : Yes',
                '  Port Auto-neg Advertised Cap (Hex) : 0000',
                '  Port MAU Type                      : 35',
                ''
                ' Link Aggregation',
                '  Link Aggregation Capable : Yes',
                '  Link Aggregation Enable  : No',
                '  Link Aggregation Port ID : 0',
                '',
                ' Max Frame Size : 1526',
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
            'LLDP Remote Devices Information',
            ' Local Port Chassis ID        Port ID           System Name',
            ' ---------- ----------------- -----------------'
            ' ------------------------------',
        ]

        port_template = ' {:<10} {:<17} {:<17} {:s}'

        for key, remote_mac in self.__connections.iteritems():
            normalized_mac = remote_mac.replace(
                ":",
                "-",
            )

            output += [
                port_template.format(
                    key,
                    '00-00-00-00-00-00',
                    normalized_mac,
                    "simulator",
                )
            ]

        output += (
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
            'LLDP Local Global Information',
            ' Chassis Type                : MAC Address',
            ' Chassis ID                  : 00-00-00-00-00-00',
            ' System Name                 : simulator',
            ' System Description          : simulator',
            ' System Capabilities Support : Bridge',
            ' System Capabilities Enabled : Bridge',
            ' Management Address          : 0.0.0.0 (IPv4)',
            '',
            'LLDP Local Port Information',
            ' Port     Port ID Type     Port ID           Port Description',
            ' -------- ---------------- -----------------'
            ' ---------------------------------',
        ]

        port_template = ' {0:<8} Mac Address      {1:s}' \
                        ' Ethernet Port on unit 0, port {2:d}'
        step = 1
        for interface in self.__interfaces:
            iface_index = interface['ifaceIndex']
            iface_mac = interface['mac'].replace(
                ":",
                "-"
            )
            output += [
                port_template.format(
                    iface_index,
                    iface_mac,
                    step,
                )
            ]
            step += 1

        output += ['']
        return output


class ShowVlanGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, vlans):
        super(
            ShowVlanGenerator,
            self
        ).__init__()
        self.__vlans = vlans

    def _generate(self):
        def __generate_vlan_output(vlan):
            ports_output = []

            column_counter = 0
            ports_row = ''

            for port in vlan['ports']:
                ports_row += ' {0:s}(S)'.format(port)
                column_counter += 1
                if column_counter == 5:
                    ports_output.append(ports_row)
                    ports_row = ''
                    column_counter = 0

            '''
            Last row
            '''
            if column_counter < 5:
                ports_output.append(ports_row)

            id_template = "{0:s}{1:d}".format(
                '{:<23}'.format('Vlan ID:'),
                vlan['number'],
            )
            type_temlplate = '{:<23}Static'.format('Type:')
            name_template = "{0:s}{1:s}".format(
                '{:<23}'.format('Name:'),
                vlan['name'],
            )
            status_template = '{:<23}Active'.format('Status:')
            ports_template = "{0:s}{1:s}".format(
                '{:<20}'.format('Ports/Port channel:'),
                ports_output[0],
            )

            _output = [
                id_template,
                type_temlplate,
                name_template,
                status_template,
                ports_template,
            ]

            if len(ports_output) > 1:
                for ports_row in ports_output[1:]:
                    _output.append(
                        ' '*20 + ports_row
                    )

            _output.append('')
            return _output

        '''
        Generate output for "show vlan" command.
        '''
        output = reduce(
            lambda old, new: old + __generate_vlan_output(new),
            self.__vlans.values(),
            [''],
        )
        output += (
            '',
        )
        return output


class ShowInterfaceStatusGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, interfaces):
        super(
            ShowInterfaceStatusGenerator,
            self
        ).__init__()
        self.__interfaces = interfaces

    def _generate(self):
        def __generate_status_output(interface):
            header_template = 'Information of {0:s}'.format(
                interface['ifaceIndex']
            )

            _output = [header_template]
            mac_address = interface['mac']

            '''
            Map of messages, consisting of a set of tuples.
            Each tuple contains:
              - key
              - space-fill value for value padding
              - value
            '''

            message_map = [
                (' Basic information:', 19, ''),
                ('  Port type:', 26, '100TX'),
                ('  Mac address:', 26, mac_address),
                (' Configuration', 15, ''),
                ('  Name:', 7, ''),
                ('  Port admin:', 26, 'Up'),
                ('  Speed-duplex:', 26, 'Auto'),
                ('  Capabilities:', 26, '10half, 10full, 100half, 100full'),
                ('  Broadcast storm:', 26, 'Enabled'),
                ('  Broadcast storm limit:', 26, '32000 octets/second'),
                ('  Flow control:', 26, 'Disabled'),
                ('  LACP:', 26, 'Disabled'),
                ('  Port security:', 26, 'Disabled'),
                ('  Max MAC count:', 26, 0),
                ('  Port security action:', 26, 'None'),
                (' Current status:', 16, ''),
                ('  Link status:', 26, 'Up'),
                ('  Port operation status:', 26, 'Up'),
                ('  Operation speed-duplex:', 26, '100full'),
                ('    Flow control type:', 26, 'None'),
            ]

            for message_tuple in message_map:
                message = '{0:s}{1:}'.format(
                    '{key:<{padding}}'.format(
                        key=message_tuple[0],
                        padding=message_tuple[1],
                    ),
                    message_tuple[2],
                )
                _output.append(message)

            _output += (
                '',
            )

            return _output

        '''
        Generate output for "show interfaces switchport" command.
        '''
        output = reduce(
            lambda old, new: old + __generate_status_output(new),
            self.__interfaces,
            [],
        )

        return output


class ShowInterfaceSwitchPortGenerator(AvlanSimulatorBaseCommandGenerator):
    def __init__(self, interfaces):
        super(
            ShowInterfaceSwitchPortGenerator,
            self
        ).__init__()
        self.__interfaces = interfaces

    def _generate(self):
        def __generate_switchport_output(interface):
            '''
            TODO: get default vlan
            '''
            native_vlan = 1
            vlans_on_port = []
            if 'vlans' in interface:
                for vlan in interface['vlans']:
                    vlan_number = vlan['number']
                    vlans_on_port.append(vlan_number)
                    if 'pvid' in vlan and vlan['pvid'] is True:
                        native_vlan = vlan_number

            '''
            We are not differentiating between tagged and untagged vlans in
            simulation, thus "(x)" instead of "(u)" for untagged and "(t)" for
            tagged ports.
            '''
            allowed_vlans_output = []
            column_counter = 0
            allowed_vlans_row = ''
            allowed_vlans_row_count = 0
            for vlan in vlans_on_port:
                if column_counter == 0 and allowed_vlans_row_count == 0:
                    allowed_vlans_row = '{0:d}(t),'.format(vlan)
                else:
                    allowed_vlans_row += '{:>9}'.format(
                        '{0:d}(t),'.format(vlan)
                    )
                column_counter += 1
                if column_counter == 7:
                    allowed_vlans_output.append(allowed_vlans_row)
                    allowed_vlans_row = ''
                    column_counter = 0
                    allowed_vlans_row_count += 1

            '''
            Last row
            '''
            if column_counter < 7:
                allowed_vlans_output.append(allowed_vlans_row)

            header_template = 'Information of {0:s}'.format(
                interface['ifaceIndex']
            )

            _output = [header_template]

            '''
            Map of messages, consisting of a set of tuples.
            Each tuple contains:
              - key
              - space-fill value for value padding
              - value
            '''
            message_map = [
                ('Broadcast threshold:', 31, 'Enabled, 32000 octets/second'),
                ('LACP status:', 31, 'Disabled'),
                ('Ingress rate limit: disable, Level:', 36, '255'),
                ('Egress rate limit: disable, Level:', 36, '255'),
                ('VLAN membership mode:', 31, 'Hybrid'),
                ('Ingress rule:', 31, 'Enabled'),
                ('Acceptable frame type:', 31, 'All frames'),
                ('Native VLAN:', 31, native_vlan),
                ('Priority for untagged traffic:', 31, 0),
                ('GVRP status:', 31, 'Disabled'),
                ('Allowed VLAN:', 31, allowed_vlans_output[0]),
            ]

            if len(allowed_vlans_output) > 1:
                for allowed_vlans_output_row in allowed_vlans_output[1:]:
                    message_map.append(
                        ('', 13, allowed_vlans_output_row)
                    )

            message_map += (
                ('Forbidden VLAN:', 31, ''),
                ('Private-VLAN mode:', 31, 'NONE'),
                ('Private-VLAN host-association:', 31, 'NONE'),
                ('Private-VLAN mapping:', 31, 'NONE'),
            )

            for message_tuple in message_map:
                message = '{0:s}{1:}'.format(
                    ' {key:<{padding}}'.format(
                        key=message_tuple[0],
                        padding=message_tuple[1],
                    ),
                    message_tuple[2],
                )
                _output.append(message)

            _output += (
                '',
            )

            return _output

        '''
        Generate output for "show interfaces switchport" command.
        '''
        output = reduce(
            lambda old, new: old + __generate_switchport_output(new),
            self.__interfaces,
            [],
        )

        return output


class AvlanSimulatorEdgeCoreMock(AvlanSimulatorBaseMock):
    '''
    Dynamically construct methods and config basing on passed dictionary
    '''

    '''
    TODO: add 'show interfaces switchport <port>' command (currently handled
    using caching)
    '''
    def __init__(self, config):
        super(
            AvlanSimulatorEdgeCoreMock,
            self
        ).__init__(
            config=config,
        )

        self._command_output_mapping = {
            'show_vlan': ShowVlanGenerator(
                vlans=self._vlans,
            ),
            'show_interfaces_switchport': ShowInterfaceSwitchPortGenerator(
                interfaces=self._interfaces,
            ),
            'show_interfaces_status': ShowInterfaceStatusGenerator(
                interfaces=self._interfaces,
            ),
            'show_lldp_info_local_device': ShowLLDPInfoLocalDeviceGenerator(
                interfaces=self._interfaces,
            ),
            'show_lldp_info_remote_device': ShowLLDPInfoRemoteDeviceGenerator(
                connections=self._connection_map,
            ),
            'show_lldp_info_remote_detail':
                ShowLLDPInfoRemoteDetailGenerator(
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
                    "show vlan",
                    "show interface status",
                    "show interfaces switchport",
                    "show lldp info local-device",
                    "show lldp info remote-device",
                    "show lldp info remote detail <port>",
                    "",
                    "lldp info remote detail ports: {0:s}".format(
                        reduce(
                            lambda old, new: "{0:s}, {1:s}".format(
                                str(old),
                                str(new),
                            ),
                            connection_map.keys(),
                            '',
                        )
                    ),
                )

                arguments_count = len(self.args)
                is_show_vlan = (
                    arguments_count == 1
                    and self.args[0] == 'vlan'
                )
                is_show_interfaces_switchport = (
                    arguments_count == 2
                    and ' '.join(self.args) == 'interfaces switchport'
                )
                is_show_interfaces_status = (
                    arguments_count == 2
                    and ' '.join(self.args) == 'interface status'
                )
                is_show_lldp_info_local_device = (
                    arguments_count == 3
                    and ' '.join(self.args) == 'lldp info local-device'
                )
                is_show_lldp_info_remote_device = (
                    arguments_count == 3
                    and ' '.join(self.args) == 'lldp info remote-device'
                )
                is_show_lldp_info_remote_detail = (
                    arguments_count > 3
                    and ' '.join(self.args[:4]) == 'lldp info remote detail'
                    and ' '.join(self.args[4:]) in connection_map.keys()
                )

                if is_show_vlan:
                    output = command_output_mapping['show_vlan'].output
                elif is_show_interfaces_switchport:
                    output = command_output_mapping[
                        'show_interfaces_switchport'
                    ].output
                elif is_show_interfaces_status:
                    output = command_output_mapping[
                        'show_interfaces_status'
                    ].output
                elif is_show_lldp_info_local_device:
                    output = command_output_mapping[
                        'show_lldp_info_local_device'
                    ].output
                elif is_show_lldp_info_remote_device:
                    output = command_output_mapping[
                        'show_lldp_info_remote_device'
                    ].output
                elif is_show_lldp_info_remote_detail:
                    try:
                        output = command_output_mapping[
                            'show_lldp_info_remote_detail'
                        ].output[' '.join(self.args[4:])]
                    except KeyError:
                        output = help_msg
                else:
                    output = help_msg

                for line in output:
                    self.writeln(line)
                self.exit()
        self._commands.append(CommandShow)
