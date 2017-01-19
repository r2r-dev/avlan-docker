from src.applications.auth.controller.AvlanAuthorizedController import (
    AvlanAuthorizedController
)
from src.applications.config.api.AvlanConfigApi import AvlanConfigApi
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery
#from src.applications.config.view.AvlanConfigDownloadView import (
#    AvlanConfigDownloadView
#)


from webob import Response


class AvlanConfigDownloadController(AvlanAuthorizedController):
    def get(self, config_id):
        config_api = AvlanConfigApi(self.dao)
        config = config_api.get_config_path(id=config_id)

        response = Response(
            content_type='application/json',
            content_disposition='attachment; filename={0:s}'.format(
                config['filename']
            ),
        )
        response.body = open(
            config['path'],
            'rb'
        ).read()

        return response
