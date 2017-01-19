from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyNodeCreateView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyNodeCreateTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Node"
        self.name = "Name"
        self.type = "Type"
        self.save = "Save"
        self.close = "Close"
        self.ip = "IP Address"
        self.ssh_port = "SSH Port"
        self.ssh_username = "SSH Username"
        self.ssh_password = "SSH Password"
        self.message = None
        self.error = None
