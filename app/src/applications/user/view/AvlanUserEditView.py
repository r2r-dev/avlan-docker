from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanUserEditView(AvlanBaseView):
    __template = 'webroot/html/AvlanUserEditTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "User"
        self.username = "Username"
        self.password = "Password"
        self.language = "Language"
        self.color = "Color"
        self.close = "Close"
        self.save = "Save"

        self.message = None
        self.error = None

        self._settings = None
        self._user_settings = None
        self._user = None
