from src.applications.base.application.AvlanBaseApplication import AvlanBaseApplication
from src.applications.auth.controller.AvlanAuthRegisterApiController import AvlanAuthRegisterApiController
from src.applications.auth.controller.AvlanAuthLoginApiController import AvlanAuthLoginApiController
from src.applications.auth.controller.AvlanAuthLogoutApiController import AvlanAuthLogoutApiController


class AvlanAuthApiApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'register',
            '/api/auth/register',
            controller=AvlanAuthRegisterApiController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        self.mapper.connect(
            'login',
            '/api/auth/login',
            controller=AvlanAuthLoginApiController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        self.mapper.connect(
            'login',
            '/api/auth/logout',
            controller=AvlanAuthLogoutApiController,
            conditions=dict(method=["GET"]),
            action='GET',
        )
