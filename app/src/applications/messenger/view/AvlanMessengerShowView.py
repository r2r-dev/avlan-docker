from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanMessengerShowView(AvlanBaseView):
    __template = 'webroot/html/AvlanMessengerShowTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.command = None
        self.output = None
        self.ip = None
        self.name = None