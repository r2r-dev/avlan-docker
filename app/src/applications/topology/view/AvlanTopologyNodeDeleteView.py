from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyNodeDeleteView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyNodeDeleteTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Config"
        self.close = "Close"
        self.delete = "Delete"

        self.message = None
        self.error = None
        self._node_id = None
