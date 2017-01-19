from src.applications.base.application.AvlanBaseApplication import\
    AvlanBaseApplication
from src.applications.user.controller.AvlanUserListApiController import\
    AvlanUserListApiController


class AvlanUserApiApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'user',
            '/api/user/',
            controller=AvlanUserListApiController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        '''
        self.mapper.connect(
            'user',
            '/api/user/{id}',
            controller=AvlanUserShowApiController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'user',
            '/api/user/{id}/edit',
            controller=AvlanUserEditApiController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        self.mapper.connect(
            'user',
            '/api/user/{id}/delete',
            controller=AvlanUserDeleteApiController,
            conditions=dict(method=["DELETE"]),
            action='delete',
        )
        '''
