from os.path import exists as path_exists
from os import makedirs

from shutil import copyfileobj
from cgi import FieldStorage
from src.applications.base.api.AvlanBaseApi import (
    AvlanBaseApi,
    jsonize,
)
from src.applications.user.storage.AvlanUserStorage import AvlanUserStorage
from src.applications.user.query.AvlanUserQuery import AvlanUserQuery
from src.applications.setting.query.AvlanSettingQuery import AvlanSettingQuery

from passlib.hash import pbkdf2_sha1


class AvlanUserApi(AvlanBaseApi):
    def create_user(self, username, password):
        hashed_password = self.__hash_password(
            username,
            password,
        )

        user_query = AvlanUserQuery(self._dao)
        user = user_query.create_user(
            username=username,
            password=hashed_password,
        )

        settings_query = AvlanSettingQuery(self._dao)
        settings_query.create_user_settings(
            user_id=user.id,
        )

        user_image_directory = 'webroot/img/user/{0:d}'.format(user.id)
        if not path_exists(user_image_directory):
            makedirs(user_image_directory)

    def delete_user(self):
        pass

    def list_users(self):
        example_user = AvlanUserStorage()
        users = self._dao.list(example_user)
        return users

    def get_user(self, id=None, username=None, password=None):
        hashed_password = None
        if password is not None:
            hashed_password = self.__hash_password(
                username,
                password,
            )

        user_query = AvlanUserQuery(self._dao)
        user = user_query.get_user(
            id=id,
            username=username,
            password=hashed_password,
        )
        return user

    @jsonize
    def update_user(self, user_id, payload):
        user_query = AvlanUserQuery(self._dao)
        settings_query = AvlanSettingQuery(self._dao)

        user = user_query.get_user(
            id=user_id,
        )

        username = payload['username']
        password = payload['password']
        if len(password) > 0:
            user.password = self.__hash_password(
                username,
                password,
            )

        self._dao.update(user)

        image_id = payload['image_id']
        image = payload['image']
        if isinstance(image, FieldStorage) and "image" in image.type:
            if image_id == '':
                # TODO: use random string
                image_id = user_id

            with open(
                    'webroot/img/user/{0}/avatar'.format(user_id),
                    'wb'
            ) as fout:
                copyfileobj(
                    image.file,
                    fout,
                    100000,
                )

        # TODO, make setting options more generic
        options = {
            'language': payload['language'],
            'color': payload['color'],
            'image': image_id,
        }

        settings_query.set_user_settings(
            user_id=user_id,
            options=options,
        )

        return

    def __hash_password(self, username, password):
        count = 0
        salt = ''
        for char in username:
            # every second character is added to salt
            if count % 2 == 0:
                salt += char
            count += 1

        salt = bytes(salt)
        hashed_password = pbkdf2_sha1.encrypt(
            password,
            salt=salt,
        )
        return hashed_password
