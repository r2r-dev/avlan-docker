from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanUserListView(AvlanBaseView):
    __template = 'webroot/html/AvlanUserListTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "User List"
        self._users = {}
        self._users_settings = {}
