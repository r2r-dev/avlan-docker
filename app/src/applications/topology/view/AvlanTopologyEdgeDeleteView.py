from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyEdgeDeleteView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyEdgeDeleteTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Node"
        self.source_node = "Source Node"
        self.source_interface = "Source Interface"
        self.target_node = "Connected Node"
        self.target_interface = "Connected Interface"
        self.delete = "Delete"
        self.close = "Close"

        self.message = None
        self.error = None
        self._source_node = None
        self._source_interfaces = None
        self._target_node = None
        self._target_interface = None
