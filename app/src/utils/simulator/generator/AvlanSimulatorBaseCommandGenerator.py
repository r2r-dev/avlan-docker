from abc import (
    ABCMeta,
    abstractmethod,
)


class AvlanSimulatorBaseCommandGenerator(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        self._output = None
        pass

    @property
    def output(self):
        if self._output is None:
            self._output = self._generate()
        return self._output

    @abstractmethod
    def _generate(self):
        pass
