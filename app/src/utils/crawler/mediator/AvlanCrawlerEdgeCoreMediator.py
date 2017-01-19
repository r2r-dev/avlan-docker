from binascii import unhexlify
from re import (
    compile as re_compile,
    search as re_search,
    DOTALL,
    IGNORECASE,
    MULTILINE,
)

from src.utils.crawler.utils import MACAddressParameter
from src.utils.crawler.mediator.AvlanCrawlerBaseMediator import (
    AvlanCrawlerBaseMediator,
)


class AvlanCrawlerEdgeCoreMediator(AvlanCrawlerBaseMediator):
    __additional_connection_parameters = {
        'kex_cipher': 'diffie-hellman-group1-sha1',
        'key_cipher': 'ssh-dss'
    }

    lldp_local_pattern = re_compile(
        r"^\s*Eth(.+?)\s*MAC Address\s+(\S+).+?$",
        MULTILINE | DOTALL
    )

    lldp_neighbour_pattern = re_compile(
        r"(?P<local_if>Eth\s\S+)\s+(\||)\s+(?P<id>\S+).*?(?P<name>\S+)$",
        MULTILINE | IGNORECASE
    )

    lldp_detail_pattern = re_compile(
        r".*Chassis I(d|D)\s+:\s(?P<id>\S+).*?Port(|\s+)ID Type\s+:\s"
        r"(?P<p_type>[^\n]+).*?Port(|\s+)ID\s+:\s(?P<p_id>[^\n]+).*?"
        r"Sys(|tem\s+)Name\s+:\s(?P<name>\S+).*?"
        r"(SystemCapSupported|System\sCapabilities)\s+:\s"
        r"(?P<capability>[^\n]+).*",
        MULTILINE | IGNORECASE | DOTALL
    )

    interface_pattern = re_compile(
        r"Information of (?P<interface>[^\n]+?)\n",
        MULTILINE | IGNORECASE | DOTALL
    )

    interface_swport_pattern = re_compile(
        r"Information of (?P<interface>[^\n]+?)\n.*?"
        r"VLAN Membership Mode(|\s+):\s+(?P<mode>[^\n]+?)\n.*?"
        r"Native VLAN(|\s+):\s+(?P<native>\d+).*?"
        r"Allowed VLAN(|\s+):\s+(?P<vlans>.*?)"
        r"Forbidden VLAN(|\s+):",
        MULTILINE | IGNORECASE | DOTALL
    )

    vlan_pattern = re_compile(
        r"^VLAN ID\s*?:\s+?(?P<vlan_id>\d{1,4})\n"
        r".*?Name\s*?:\s+(?P<name>\S*?)\n",
        IGNORECASE | DOTALL | MULTILINE
    )

    interface_status_pattern = re_compile(
        r"Information of (?P<interface>[^\n]+?)\n.*?"
        r"Mac Address(|\s+):\s+(?P<mac>[^\n]+?)\n(?P<block>.*)",
        MULTILINE | IGNORECASE | DOTALL
    )

    def _send_command(self, command, **kwargs):
        return super(
            AvlanCrawlerEdgeCoreMediator,
            self
        )._send_command(
            command=command,
            page_string='---More---',
        )

    def get_lldp_neighbors(self):
        local_interface_macs = self.get_interfaces_macs()
        results = {}

        '''
        Preserve for debugging purposes.

        local_port_ids = {}  # name -> id
        local_info = self._send_command("show lldp info local-device")
        for port, local_id in self.lldp_local_pattern.findall(local_info):
            local_port_ids["Eth" + port] = MACAddressParameter().clean(
                local_id
            )
        '''

        command_output = self._send_command("show lldp info remote-device")

        for if_match in self.lldp_neighbour_pattern.finditer(command_output):
            local_interface = if_match.group("local_if")

            '''
            if local_interface not in local_port_ids:
                continue
            '''
            if local_interface not in local_interface_macs:
                continue

            source_mac = local_interface_macs[local_interface]

            interface_details = self._send_command(
                "show lldp info remote detail {0:}".format(local_interface)
            )

            match = re_search(
                self.lldp_detail_pattern,
                interface_details
            )

            neighbor_mac = ''
            if match:
                '''
                Determine remote port type
                '''
                port_subtype = {
                    "MAC Address": 3,
                    "Interface name": 5,
                    "Interface Name": 5,
                    "Inerface Alias": 5,
                    "Inerface alias": 5,
                    "Interface Alias": 5,
                    "Interface alias": 5,
                    "Local": 7
                }[match.group("p_type")]

                if port_subtype == 3:
                    remote_port = MACAddressParameter().clean(
                        match.group("p_id")
                    )
                elif port_subtype == 5:
                    remote_port = match.group("p_id").strip()
                else:
                    # Removing bug
                    remote_port = unhexlify(
                        ''.join(
                            match.group("p_id").split('-')
                        )
                    )
                    remote_port = remote_port.rstrip('\x00')
                try:
                    neighbor_mac = MACAddressParameter().clean(
                        remote_port
                    )
                except ValueError:
                    continue

            results[source_mac] = neighbor_mac
        return results

    def get_vlans_names(self):
        results = {}
        output = self._send_command(
            'show vlan',
        )

        for match in self.vlan_pattern.finditer(output):
            results[int(match.group("vlan_id"))] = match.group("name")

        return results

    def get_interfaces_vlans(self):
        results = {}
        output = self._send_command('show interfaces switchport')

        for block in output.rstrip("\n\n").split("\n\n"):
            matchint = self.interface_pattern.search(block)
            interface = matchint.group("interface")
            swport_details = {
                "pvid": "",
                "vlans": [],
            }

            if re_search(
                    r"Member port of trunk \d+",
                    block,
            ):
                # skip portchannel members
                results[interface] = swport_details
                continue

            match = self.interface_swport_pattern.search(block)
            swport_details['pvid'] = int(match.group("native"))
            pattern = re_compile("\)([^,]+?)(\d)")
            vlans = pattern.sub(
                r"),\g<2>",
                match.group("vlans").rstrip(",\n ")
            )
            vlans = vlans.replace(
                " ",
                ""
            )
            vlans_list = []
            for i in vlans.split(","):
                m = re_search(
                    "(?P<vlan>\d+)\((?P<tag>u|t)\)",
                    i
                )
                vlans_list += [int(m.group("vlan"))]
            swport_details["vlans"] = vlans_list

            results[interface] = swport_details

        return results

    def get_interfaces_macs(self):
        results = {}
        output = self._send_command("show interface status")
        buf = output.lstrip("\n\n")
        for l in buf.split("\n\n"):
            match = self.interface_status_pattern.search(l + "\n")
            if match:
                interface = match.group("interface")
                results[interface] = MACAddressParameter().clean(
                    match.group("mac")
                )

        return results

    def fetch_remote_data(self):
        interfaces_vlans = self.get_interfaces_vlans()
        interfaces_macs = self.get_interfaces_macs()
        vlans_names = self.get_vlans_names()

        extracted_interfaces = []

        for interface_index, mac in interfaces_macs.iteritems():
            extracted_interface = {
                'ifaceIndex': interface_index,
                'mac': mac,
                'vlans': [],
            }

            try:
                vlans_on_interface = interfaces_vlans[interface_index]
            except KeyError:
                '''
                We have encountered trunk port.
                '''
                continue

            for vlan_id_on_interface in vlans_on_interface['vlans']:
                extracted_interface['vlans'].append(
                    {
                        'number': vlan_id_on_interface,
                        'name': vlans_names[vlan_id_on_interface],
                        'pvid': (
                            vlans_on_interface['pvid'] == vlan_id_on_interface
                        )
                    }
                )

            extracted_interfaces += [extracted_interface]

        '''
        Merge two lists. One from extracted interfaces, other with already
        discovered, existing within configuration.
        '''

        for extracted_interface in extracted_interfaces:
            found_interface = None
            for interface_in_node in self._node['interfaces']:
                if (
                    extracted_interface['ifaceIndex'] ==
                    interface_in_node['ifaceIndex']
                ):
                    found_interface = interface_in_node
                    break

            if found_interface is None:
                self._node['interfaces'] += [extracted_interface]
                continue

            found_interface['vlans'] = extracted_interface['vlans']
            found_interface['mac'] = extracted_interface['mac']
