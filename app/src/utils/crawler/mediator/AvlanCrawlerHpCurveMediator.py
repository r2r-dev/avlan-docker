from re import (
    search as re_search,
    compile as re_compile,
    DOTALL,
    IGNORECASE,
    MULTILINE,
)

from src.utils.crawler.utils import MACAddressParameter
from src.utils.crawler.mediator.AvlanCrawlerBaseMediator import (
    AvlanCrawlerBaseMediator,
    RemoteDataUnavailableException,
)


class AvlanCrawlerHpCurveMediator(AvlanCrawlerBaseMediator):
    vlan_pattern = re_compile('^\s{2}(\S+)\s+(.+)\|')

    lldp_local_pattern = re_compile(
        r"^\s*(\S+)\s*\|\s*local\s+(\d+)\s+.+?$",
        MULTILINE
    )

    lldp_split_pattern = re_compile(
        r"^\s*----.+?\n",
        MULTILINE | DOTALL
    )

    lldp_line_pattern = re_compile(
        r"^\s*(?P<port>\S+)\s*|",
        MULTILINE | DOTALL
    )

    lldp_port_id_pattern = re_compile(
        r"PortType\s*:\s*(\S+).+?PortId\s*:\s*([a-zA-Z0-9\.\- ]+)",
        MULTILINE | DOTALL | IGNORECASE
    )

    interface_mac_pattern = re_compile(
        r"Status and Counters - Port Counters for port (?P<port>[^\n]+?)"
        r"\n\n.*[^\n]\n.*?address\s+:\s+(?P<mac>\S+)",
        MULTILINE | IGNORECASE
    )

    def get_interfaces_macs(self):
        results = {}
        output = self._send_command('show interfaces all')
        for block in output.rstrip("\n\n\n").split("\n\n\n"):
            match = self.interface_mac_pattern.search(block)
            if match:
                interface = match.group("port").rstrip()
                results[interface] = MACAddressParameter().clean(
                    match.group("mac")
                )
        return results

    def get_interfaces_pvids(self):
        output = self._send_command('show interfaces status')

        output_lines = output.split('\n')
        if not output_lines[0].startswith('  Port'):
            raise RemoteDataUnavailableException(
                self._node['ip'],
                'interfaces',
                output,
            )

        result = {}

        for line in output_lines[2:]:
            fields = line.split()
            interface_index = fields[0]
            pvid = fields[-1]
            result[interface_index] = int(pvid)

        return result

    def get_interfaces_vlans(self, interfaces):
        result = {}

        for interface in interfaces:
            output = self._send_command(
                'show vlans port {0}'.format(interface)
            )

            output_lines = output.split('\n')
            if not output_lines[1].startswith(' Status'):
                raise RemoteDataUnavailableException(
                    self._node['ipAddress'],
                    'vlans',
                    output,
                )

            vlans = []
            '''
            TODO: what if vlan has no name?
            '''
            for line in output_lines[4:]:
                match = self.vlan_pattern.match(line)
                if match is None:
                    continue

                vlans.append(
                    {
                        'number': int(match.group(1)),
                        'name': match.group(2).strip(),
                    }
                )

            result[interface] = vlans
        return result

    def get_lldp_neighbors(self):
        local_interface_macs = self.get_interfaces_macs()
        results = {}

        '''
        Preserve for debugging purposes.

        local_port_ids = {}  # name -> id
        local_info = self._send_command("show lldp info local-device")
        for port, local_id in self.lldp_local_pattern.findall(local_info):
            local_port_ids[port] = local_id
        '''

        remote_info = self._send_command("show lldp info remote-device")
        r_splits = self.lldp_split_pattern.split(remote_info)[1].splitlines()
        for r_split in r_splits:
            r_split = r_split.strip()
            if not r_split:
                continue
            if_match = self.lldp_line_pattern.search(r_split)
            if not if_match:
                continue

            local_interface = if_match.group("port")

            '''
            if local_interface not in local_port_ids:
                continue
            '''
            if local_interface not in local_interface_macs:
                continue

            source_mac = local_interface_macs[local_interface]

            interface_details = self._send_command(
                "show lldp info remote-device {0:}".format(local_interface)
            )

            # Get remote port
            match = re_search(
                self.lldp_port_id_pattern,
                interface_details
            )

            if not match:
                continue

            remote_port_id_subtype = {
                "mac-...": 4,
                "local": 7,  # @todo: check
            }[match.group(1)]

            remote_port_id = match.group(2)
            if remote_port_id_subtype == 4:
                remote_port_id = remote_port_id.rstrip().replace(
                    ' ',
                    ':',
                )
            else:
                remote_port_id = remote_port_id.strip()

            try:
                results[source_mac] = MACAddressParameter().clean(
                    remote_port_id
                )
            except ValueError:
                continue

        return results

    def fetch_remote_data(self):
        '''
        TODO: Do not rely on 'Primary Vlan global setting'
        '''
        interfaces_pvids = self.get_interfaces_pvids()
        interfaces_macs = self.get_interfaces_macs()
        interfaces_vlans = self.get_interfaces_vlans(interfaces_pvids.keys())

        extracted_interfaces = []

        for interface_index, pvid_on_interface in interfaces_pvids.iteritems():
            extracted_interface = {
                'ifaceIndex': interface_index,
                'mac': interfaces_macs[interface_index],
                'vlans': [],
            }

            try:
                vlans_on_interface = interfaces_vlans[interface_index]
            except KeyError:
                '''
                We have encountered trunk port.
                '''
                continue

            for vlan_on_interface in vlans_on_interface:
                vlan_number_on_interface = vlan_on_interface['number']
                extracted_interface['vlans'].append(
                    {
                        'number': vlan_number_on_interface,
                        'name': vlan_on_interface['name'],
                        'pvid': (
                            pvid_on_interface ==
                            vlan_number_on_interface
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
