from src.applications.base.application.AvlanBaseApplication import \
    AvlanBaseApplication
from src.applications.auth.application.AvlanAuthApiApplication import \
    AvlanAuthApiApplication
from src.applications.user.application.AvlanUserApiApplication import \
    AvlanUserApiApplication


class AvlanDispatcherApiApplication(AvlanBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'auth',
            '/api/auth{path_info:.*}',
            app=AvlanAuthApiApplication,
        )
        self.mapper.connect(
            'user',
            '/api/user{path_info:.*}',
            app=AvlanUserApiApplication,
        )

    def _get_route(self, **kwargs):
        match = kwargs['match']
        return match['app'](**self.config)
