from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyNodeShowView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyNodeShowTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Node"
        self.name = "Name"
        self.id = "Id"
        self.close = "Close"
        self.interface = "Interface"
        self.ipAddress = "IP Address"
        self.vlans = "Vlans"
        self.vlan = "Vlan"
        self.interfaces = "Interfaces"
        self.interface = "Interface"
        self.details = "Node Details"
        self.vlans_interface = "Vlans on Interface"
        self.interfaces_vlan = "Interfaces with Vlan"
        self._node = None
        self._interfaces = None
        self._vlans = None
