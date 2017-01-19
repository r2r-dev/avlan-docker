from src.applications.base.application.AvlanBaseApplication import AvlanBaseApplication
from src.applications.auth.controller.AvlanAuthLoginController import AvlanAuthLoginController
from src.applications.auth.controller.AvlanAuthLogoutController import AvlanAuthLogoutController
from src.applications.auth.controller.AvlanAuthRegisterController import AvlanAuthRegisterController


class AvlanAuthApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'auth',
            '/auth/login',
            controller=AvlanAuthLoginController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'auth',
            '/auth/login',
            controller=AvlanAuthLoginController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        self.mapper.connect(
            'auth',
            '/auth/register',
            controller=AvlanAuthRegisterController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'auth',
            '/auth/register',
            controller=AvlanAuthRegisterController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        self.mapper.connect(
            'auth',
            '/auth/logout',
            controller=AvlanAuthLogoutController,
            conditions=dict(method=["GET"]),
            action='get',
        )
