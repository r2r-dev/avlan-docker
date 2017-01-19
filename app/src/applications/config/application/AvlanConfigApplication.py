from src.applications.base.application.AvlanBaseApplication import AvlanBaseApplication
from src.applications.config.controller.AvlanConfigListController import AvlanConfigListController
from src.applications.config.controller.AvlanConfigImportController import AvlanConfigImportController
from src.applications.config.controller.AvlanConfigDeleteController import AvlanConfigDeleteController
#from src.applications.user.controller.AvlanConfigShowController import AvlanConfigShowController
#from src.applications.user.controller.AvlanConfigEditController import AvlanConfigEditController
from src.applications.config.controller.AvlanConfigRunController import AvlanConfigRunController
from src.applications.config.controller.AvlanConfigDownloadController import (
    AvlanConfigDownloadController
)
from src.applications.config.controller.AvlanConfigLoadController import (
    AvlanConfigLoadController
)
from src.applications.config.controller.AvlanConfigCreateController import (
    AvlanConfigCreateController
)


class AvlanConfigApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'config',
            '/config/',
            controller=AvlanConfigListController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        '''
        self.mapper.connect(
            'config',
            '/config/{config_id}',
            controller=AvlanConfigShowController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'config',
            '/config/{config_id}/edit',
            controller=AvlanConfigEditController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'config',
            '/config/{config_id}/edit',
            controller=AvlanConfigEditController,
            conditions=dict(method=["POST"]),
            action='post',
        )'''
        self.mapper.connect(
            'config',
            '/config/{config_id}/run',
            controller=AvlanConfigRunController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'config',
            '/config/{config_id}/load',
            controller=AvlanConfigLoadController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'config',
            '/config/{config_id}/delete',
            controller=AvlanConfigDeleteController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'config',
            '/config/{config_id}/download',
            controller=AvlanConfigDownloadController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'config',
            '/config/{config_id}/delete',
            controller=AvlanConfigDeleteController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        self.mapper.connect(
            'config',
            '/config/import',
            controller=AvlanConfigImportController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'config',
            '/config/import',
            controller=AvlanConfigImportController,
            conditions=dict(method=["POST"]),
            action='post',
        )
        self.mapper.connect(
            'config',
            '/config/create',
            controller=AvlanConfigCreateController,
            conditions=dict(method=["GET"]),
            action='get',
        )
        self.mapper.connect(
            'config',
            '/config/create',
            controller=AvlanConfigCreateController,
            conditions=dict(method=["POST"]),
            action='post',
        )
