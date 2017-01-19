from src.applications.auth.application.AvlanAuthApplication import \
    AvlanAuthApplication
from src.applications.base.application.AvlanBaseApplication import \
    AvlanBaseApplication
from src.applications.dispatcher.application.AvlanDispatcherApiApplication \
    import AvlanDispatcherApiApplication
from src.applications.home.application.AvlanHomeApplication \
    import AvlanHomeApplication
from src.applications.user.application.AvlanUserApplication \
    import AvlanUserApplication
from src.applications.config.application.AvlanConfigApplication \
    import AvlanConfigApplication
from src.applications.topology.application.AvlanTopologyApplication \
    import AvlanTopologyApplication
from src.applications.messenger.application.AvlanMessengerApplication \
    import AvlanMessengerApplication
from src.utils.dao.AvlanSQLDao import AvlanSQLDao

from redis import StrictRedis

from src.conf import settings


class AvlanDispatcherApplication(AvlanBaseApplication):
    def __init__(self, **config):
        AvlanBaseApplication.__init__(
            self,
            **config
        )

        dao = AvlanSQLDao(
            host=settings.db_host,
            port=settings.db_port,
            username=settings.db_username,
            password=settings.db_password,
            database=settings.db_database,
            keepalive=False,
            autocommit=True,
        )

        redis = StrictRedis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
        )

        self._dispatch_config = {
            'dao': dao,
            'redis': redis,
        }

    def _set_routes(self):
        self.mapper.connect(
            '',
            '/',
            app=AvlanHomeApplication,
        )
        self.mapper.connect(
            'api',
            '/api{path_info:.*}',
            app=AvlanDispatcherApiApplication,
        )
        self.mapper.connect(
            'auth',
            '/auth{path_info:.*}',
            app=AvlanAuthApplication,
        )
        self.mapper.connect(
            'user',
            '/user{path_info:.*}',
            app=AvlanUserApplication,
        )
        self.mapper.connect(
            'config',
            '/config{path_info:.*}',
            app=AvlanConfigApplication,
        )
        self.mapper.connect(
            'topology',
            '/topology{path_info:.*}',
            app=AvlanTopologyApplication,
        )
        self.mapper.connect(
            'messenger',
            '/messenger{path_info:.*}',
            app=AvlanMessengerApplication,
        )

    def _get_route(self, **kwargs):
        match = kwargs['match']
        return match['app'](**self._dispatch_config)
