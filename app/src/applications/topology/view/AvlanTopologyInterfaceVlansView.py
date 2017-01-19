from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyInterfaceVlansView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyInterfaceVlansTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Vlans on interface"
        self.name = "Name"
        self.number = "Number"
        self.pvid = "PVID"
        self._vlans = None
