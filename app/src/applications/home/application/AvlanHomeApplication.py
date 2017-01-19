from src.applications.base.application.AvlanBaseApplication import\
    AvlanBaseApplication
from src.applications.home.controller.AvlanHomeController import\
    AvlanHomeController


class AvlanHomeApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            '',
            '/',
            controller=AvlanHomeController,
            conditions=dict(method=["GET"]),
            action='get',
        )
