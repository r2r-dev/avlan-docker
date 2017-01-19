from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanAuthRegisterView(AvlanBaseView):
    __template = 'webroot/html/AvlanAuthRegisterTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.register = "Register"
        self.login = "Login"
        self.username = "Username"
        self.password = "Password"
        #self.password_confirm = "Confirm Password"
