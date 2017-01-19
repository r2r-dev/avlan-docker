from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyNodeAvailableInterfacesView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyNodeAvailableInterfacesTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Available interfaces"
        self._available_interfaces = None
