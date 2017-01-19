from abc import (
    ABCMeta,
    abstractmethod,
)
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException


class AvlanCrawlerBaseMediator(object):
    __metaclass__ = ABCMeta
    __additional_connection_parameters = {}

    def __init__(self, node, messenger=None):
        self._node = node
        self._command_cache = {}
        self._connection = None
        self.__messenger = messenger

    def _connect(self):
        def merge_two_dicts(x, y):
            z = x.copy()
            z.update(y)
            return z

        options = {
            'device_type': self._node['type'],
            'ip': self._node['ipAddress'],
            'port': self._node['sshPort'],
            'username': self._node['sshUsername'],
            'password': self._node['sshPassword'],
        }
        try:
            self._connection = ConnectHandler(**options)
        except SSHException:
            '''
            TODO: verify if reloading paramiko preferred ciphers propagates
            to the rest of connections
            '''
            self._connection = ConnectHandler(
                **merge_two_dicts(
                    options,
                    self.__additional_connection_parameters,
                )
            )

    def _send_command(self, command, **kwargs):
        if self._connection is None:
            self._connect()

        if command not in self._command_cache:
            output = self._connection.send_command(
                command,
                **kwargs
            )
            self._command_cache[command] = output

        if self.__messenger is not None:
            self.__messenger.set(
                'ip',
                self._node['ipAddress']
            )
            self.__messenger.set(
                'name',
                self._node['name'],
            )
            self.__messenger.set(
                'command',
                command,
            )
            self.__messenger.set(
                'output',
                self._command_cache[command]
            )

        return self._command_cache[command]

    @abstractmethod
    def fetch_remote_data(self):
        pass

    @abstractmethod
    def get_lldp_neighbors(self):
        pass


class RemoteDataUnavailableException(Exception):
    def __init___(self, ip, resource, output):
        Exception.__init__(
            self,
            "Could not extract remote data: {0:s} from host: {1:s}"
            "Remote host output: {2:s}".format(
                resource,
                ip,
                output,
            )
        )
        self.ip = ip
        self.resource = resource
        self.output = output
