from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyEdgeCreateView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyEdgeCreateTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Node"
        self.source_node = "Source Node"
        self.source_interface = "Source Interface"
        self.target_node = "Target Node"
        self.target_interface = "Target Interface"
        self.save = "Save"
        self.close = "Close"
        self.message = None
        self.error = None
        self._source_node = None
        self._source_interfaces = None
        self._target_nodes = None
        self._target_interfaces = None
