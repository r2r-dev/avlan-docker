from src.applications.base.application.AvlanBaseApplication import\
    AvlanBaseApplication
from src.applications.user.controller.AvlanUserListController import\
    AvlanUserListController
from src.applications.user.controller.AvlanUserShowController import\
    AvlanUserShowController
from src.applications.user.controller.AvlanUserEditController import\
    AvlanUserEditController


class AvlanUserApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'user',
            '/user/',
            controller=AvlanUserListController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'user',
            '/user/{user_id}',
            controller=AvlanUserShowController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'user',
            '/user/{user_id}/edit',
            controller=AvlanUserEditController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'user',
            '/user/{user_id}/edit',
            controller=AvlanUserEditController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        '''
        self.mapper.connect(
            'user',
            '/user/{id}/delete',
            controller=AvlanUserDeleteController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'user',
            '/user/{id}/delete',
            controller=AvlanUserDeleteController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        '''