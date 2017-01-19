from src.applications.base.controller.AvlanBaseController import\
    AvlanBaseController
from src.applications.auth.api.AvlanAuthApi import AvlanAuthApi
from src.applications.user.api.AvlanUserApi import AvlanUserApi


from webob import exc, Response


class AvlanAuthorizedController(AvlanBaseController):
    def __before__(self):
        # One might be authorized either via session (web) or Token (api)
        if self.request.path.startswith("/api"):
            authorization_header = self.request.authorization
            if authorization_header is None:
                # Return unauthorized
                return exc.HTTPUnauthorized()
            elif len(authorization_header) > 1 and authorization_header[0] == 'Token':
                return self.__verify_token(authorization_header[1])
            else:
                return exc.HTTPUnauthorized()
        elif 'user_id' in self.session:
            user_api = AvlanUserApi(self.dao)
            user = user_api.get_user(id=self.session['user_id'])
            if user is None:
                return self.__authorize()
            return Response()
        else:
            return self.__authorize()

    def __authorize(self):
        response = exc.HTTPMovedPermanently(location='/auth/login')
        return response

    def __verify_token(self, token):
        api = AvlanAuthApi(self.dao)
        token_valid = api.verify_token(token)
        if token_valid:
            return Response()
        return exc.HTTPUnauthorized()
