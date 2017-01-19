from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanHomeView(AvlanBaseView):
    __template = 'webroot/html/AvlanHomeTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.topology = "Topology"
        self.title = "Home Page"
        self.tasks = "Tasks"
        self.machines = "Machines"
        self.users = "Users"
        self.config = "Configurations"
        self.settings = "Settings"
        self.profile = "Profile"
        self.logout = "Logout"

        self.user = None
