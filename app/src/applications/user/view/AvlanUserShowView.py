from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanUserShowView(AvlanBaseView):
    __template = 'webroot/html/AvlanUserShowTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "User"
        self.username = "Username"
        self.id = "Id"
        self.close = "Close"
        self._user = None
