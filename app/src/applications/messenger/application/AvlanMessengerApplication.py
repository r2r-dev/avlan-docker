from src.applications.base.application.AvlanBaseApplication import\
    AvlanBaseApplication
from src.applications.messenger.controller.AvlanMessengerShowController import \
    AvlanMessengerShowController


class AvlanMessengerApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'messenger',
            '/messenger/',
            controller=AvlanMessengerShowController,
            conditions=dict(method=["GET"]),
            action='get',
        )
