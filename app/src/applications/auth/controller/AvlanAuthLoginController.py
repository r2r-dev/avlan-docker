from src.applications.base.controller.AvlanBaseController import AvlanBaseController
from src.applications.auth.api.AvlanAuthApi import AvlanAuthApi
from src.applications.auth.view.AvlanAuthLoginView import AvlanAuthLoginView
from webob import (
    Response,
    exc,
)


# Open database connection
class AvlanAuthLoginController(AvlanBaseController):
    def get(self):
        # TODO: move translations handling to BaseController
        translation = list(self.request.accept_language)[0]
        view = AvlanAuthLoginView(translation)
        response = Response()
        response.body = view.render()
        return response

    def post(self):
        params = self.request.params
        api = AvlanAuthApi(self.dao)
        request_dict = {}
        for key, value in params.items():
            request_dict[key] = value
        user_id, token_value = api.login(
            payload=request_dict,
        )

        if user_id:
            self.session['user_id'] = user_id
            response = exc.HTTPMovedPermanently(location=self.request.application_url)
            response.set_cookie(
                name='Token',
                value=token_value,
            )
            self.session.save()
            self.session.persist()
            return response
        else:
            # TODO: move translations handling to BaseController
            translation = list(self.request.accept_language)[0]
            view = AvlanAuthLoginView(translation)
            view.error = "Unauthorized"
            response = Response()
            response.body = view.render()
            #response = exc.HTTPUnauthorized()
        return response
