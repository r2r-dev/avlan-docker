from src.applications.auth.controller.AvlanAuthorizedController import\
    AvlanAuthorizedController
from src.applications.user.api.AvlanUserApi import AvlanUserApi
from webob import Response
from json import dumps


# Open database connection
class AvlanUserListApiController(AvlanAuthorizedController):
    def get(self):
        api = AvlanUserApi(self.dao)
        users = api.list_users()

        users_list = []
        for user in users:
            user_dict = {}
            for key, value in vars(user).items():
                if key.startswith("_") or key == 'password':
                    continue
                user_dict[key] = value
            users_list.append(user_dict)
        response = Response(
            body=dumps(users_list),
            content_type="application/json",
        )
        return response
