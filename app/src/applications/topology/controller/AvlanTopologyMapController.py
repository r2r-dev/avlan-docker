from src.applications.auth.controller.AvlanAuthorizedController import\
    AvlanAuthorizedController
from src.applications.topology.view.AvlanTopologyMapView import\
    AvlanTopologyMapView
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery

from webob import Response


# Open database connection
class AvlanTopologyMapController(AvlanAuthorizedController):
    def get(self):
        viewer_id = self.session['user_id']
        setting_query = AvlanSettingQuery(self.dao)

        viewer_settings = setting_query.get_user_settings(viewer_id)
        translation = viewer_settings['language']
        view = AvlanTopologyMapView(
            translation=translation,
        )

        view._full = not self.request.is_xhr

        response = Response()
        response.body = view.render()
        return response
