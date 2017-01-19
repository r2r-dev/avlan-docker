from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanAuthLoginView(AvlanBaseView):
    __template = 'webroot/html/AvlanAuthLoginTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.login = "Login"
        self.register = "Register"
        self.username = "Username"
        self.password = "Password"
        self.error = None
