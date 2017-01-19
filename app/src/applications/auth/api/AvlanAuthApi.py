from src.applications.auth.query.AvlanAuthQuery import AvlanAuthQuery
from src.applications.base.api.AvlanBaseApi import (
    AvlanBaseApi,
    jsonize,
)
from src.applications.user.api.AvlanUserApi import AvlanUserApi

from time import mktime
from datetime import (
    datetime,
    timedelta,
)

import string
import random


# TODO: do we need to return json as well, or leave it to apicontrollers?
class AvlanAuthApi(AvlanBaseApi):
    @jsonize
    def register(self, payload):
        username = payload['username']
        password = payload['password']

        user_api = AvlanUserApi(self._dao)

        user_api.create_user(
            username=username,
            password=password,
        )

        return True

    @jsonize
    def login(self, payload):
        username = payload['username']
        password = payload['password']

        user_api = AvlanUserApi(self._dao)
        user = user_api.get_user(
            username=username,
            password=password,
        )

        if not user:
            return None, None

        auth_query = AvlanAuthQuery(self._dao)
        if user.tokenId:
            token = auth_query.get_token(
                id=user.tokenId,
            )
            token_date = datetime.utcfromtimestamp(token.expirationDate)
            if token_date > datetime.now():
                return user.id, token.value

        # generate token
        token_value, token_date = self.__generate_token()

        token = auth_query.create_token(
            value=token_value,
            date=token_date,
        )

        user.tokenId = token.id
        self._dao.update(user)

        # api call returns token, whilst webapp sets cookie
        return user.id, token.value

    def verify_token(self, token_value):
        auth_query = AvlanAuthQuery(self._dao)
        token = auth_query.get_token(
            value=token_value,
        )
        if token:
            token_date = datetime.utcfromtimestamp(token.expirationDate)
            if token_date > datetime.now():
                # Possibly return authorized user id/name
                return True
        return False

    def invalidate_token(self, token_value):
        auth_query = AvlanAuthQuery(self._dao)
        token = auth_query.get_token(
            value=token_value,
        )
        token.expirationDate = 0
        self._dao.update(token)

    def __generate_token(self):
        token_value = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(50)
                              )
        token_date = datetime.now() + timedelta(hours=4)
        token_date = int(mktime(token_date.timetuple()))
        return token_value, token_date
