"""
This is how it should be used:

Execute script using provided output.json:
python simulator -c test/output.json

Log in to hosts using details specified in output.json
ssh hostname@localhost -p <port number>

hostname# show interfaces status
hostname# show vlans
hostname# show vlans ports 1
hostname#
"""

import sys
from subprocess import Popen
from twisted.python import log
from os.path import isfile
from argparse import ArgumentParser
from json import (
    dumps,
    load,
    loads,
)

from src.utils.simulator.mock.AvlanSimulatorHpMock import AvlanSimulatorHpMock
from src.utils.simulator.mock.AvlanSimulatorEdgeCoreMock import \
    AvlanSimulatorEdgeCoreMock


def main():
    log.startLogging(sys.stderr)

    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        default='output.json'
    )
    parser.add_argument(
        '-m',
        '--mock',
        default=None,
    )
    args = parser.parse_args()

    if args.mock is not None:
        mock_config = loads(args.mock)

        '''
        TODO: add validation against schema.
        '''
        host_type = mock_config['type']

        '''
        TODO: move this to factory
        '''
        if host_type == 'hp_procurve':
            '''
            We need to wrap this with OS native subprocess because Twisted
            reactor is designed to handle only one connection at time.
            '''
            AvlanSimulatorHpMock(mock_config).execute()
        elif host_type == 'edgecore':
                '''
                We need to wrap this with OS native subprocess because Twisted
                reactor is designed to handle only one connection at time.
                '''
                AvlanSimulatorEdgeCoreMock(mock_config).execute()
    else:
        config_file = args.config
        if not isfile(config_file):
            print "Input config not found"
            sys.exit(1)

        with open(config_file) as config_json:
            config = load(config_json)

        connection_map = prepare_connections(config)

        script = sys.argv[0]
        child_processes = []

        for node in config['nodes']:
            node['connection_map'] = connection_map[node['id']]
            p = Popen(
                [
                    sys.executable,
                    script,
                    '--mock',
                    dumps(node),
                ])
            child_processes.append(p)

        '''
        Gather all outputs and wait until all processes are done.
        Exiting from this thread will stop sub-processes as well.
        '''
        for cp in child_processes:
            cp.wait()


def prepare_connections(config):
    interface_map = {}
    connection_map = {}
    for node in config['nodes']:
        node_id = node['id']
        if 'interfaces' not in node:
            continue

        for interface in node['interfaces']:
            interface_map[interface['id']] = (
                node_id,
                interface
            )

    for node_id, interface in interface_map.itervalues():
        if node_id not in connection_map:
            connection_map[node_id] = dict()

        if 'peerIfaceId' not in interface:
            continue

        peer_interface_id = interface['peerIfaceId']
        peer_interface = interface_map[peer_interface_id][1]
        peer_interface_mac = peer_interface['mac']

        connection_map[node_id][interface['ifaceIndex']] = peer_interface_mac

    return connection_map
