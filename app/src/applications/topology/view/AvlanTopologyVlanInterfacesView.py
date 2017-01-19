from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyVlanInterfacesView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyVlanInterfacesTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Interfaces with Vlan"
        self.index = "Interface Index"
        self.pvid = "PVID"
        self._interfaces = None
