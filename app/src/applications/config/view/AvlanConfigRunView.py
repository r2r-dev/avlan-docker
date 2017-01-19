from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanConfigRunView(AvlanBaseView):
    __template = 'webroot/html/AvlanConfigRunTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Config"
        self.close = "Close"

        self.message = None
        self.error = None
