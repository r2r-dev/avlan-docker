from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanConfigCreateView(AvlanBaseView):
    __template = 'webroot/html/AvlanConfigCreateTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Config"
        self.name = "Title"
        self.close = "Close"
        self.save = "Save"
        self.config = "Config"

        self.message = None
        self.error = None
