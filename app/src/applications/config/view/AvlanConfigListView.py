from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanConfigListView(AvlanBaseView):
    __template = 'webroot/html/AvlanConfigListTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Config List"
        self.delete = "Delete"
        self.create = "Create"
        self._import = "Import"
        self.run = "Run"
        self._configs = {}
