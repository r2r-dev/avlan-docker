from src.applications.base.query.AvlanBaseQuery import AvlanBaseQuery
from src.applications.setting.storage.AvlanSettingStorage import \
    AvlanSettingStorage
from src.applications.setting.storage.AvlanAllowedSettingStorage import \
    AvlanAllowedSettingStorage
from src.applications.setting.storage.AvlanUserSettingStrorage import \
    AvlanUserSettingStorage


class AvlanSettingQuery(AvlanBaseQuery):
    def create_user_settings(self, user_id):
        for setting in self._dao.list(AvlanSettingStorage()):
            allowed_settings = self._dao.list_where(
                where_clause="`settingId` = %s AND `default_setting` = %s",
                clazz=AvlanAllowedSettingStorage,
                arg_list=[
                    setting.id,
                    1,
                ],
            )

            if len(allowed_settings) > 0:
                allowed_setting = allowed_settings[0].id
            else:
                allowed_setting = None

            user_setting = AvlanUserSettingStorage()
            user_setting.allowedSettingId = allowed_setting
            user_setting.settingId = setting.id
            user_setting.userId = user_id
            self._dao.save(user_setting)

    def set_user_settings(self, user_id, options):
        user_settings = self._dao.list_where(
            where_clause="userId = %s",
            clazz=AvlanUserSettingStorage,
            arg_list=[user_id]
        )

        for post_setting_name, post_setting_value in options.iteritems():
            settings = self._dao.list_where(
                where_clause="`name` = %s",
                clazz=AvlanSettingStorage,
                arg_list=[post_setting_name],
            )
            setting = settings[0]
            allowed_settings = self._dao.list_where(
                where_clause="`settingId` = %s",
                clazz=AvlanAllowedSettingStorage,
                arg_list=[setting.id],
            )

            allowed_setting_id = None
            if len(allowed_settings) > 0:
                for allowed_setting in allowed_settings:
                    if allowed_setting.value == post_setting_value:
                        allowed_setting_id = allowed_setting.id
                        post_setting_value = None

            for user_setting in user_settings:
                if user_setting.settingId == setting.id:
                    user_setting.allowedSettingId = allowed_setting_id
                    user_setting.value = post_setting_value
                    self._dao.update(user_setting)
        return

    def get_settings(self):
        settings_dict = {}
        for setting in self._dao.list(AvlanSettingStorage()):
            setting_name = setting.name
            allowed_settings = self._dao.list_where(
                where_clause="`settingId` = %s",
                clazz=AvlanAllowedSettingStorage,
                arg_list=[setting.id],
            )
            if len(allowed_settings) > 0:
                allowed_settings_list = []
                for allowed_setting in allowed_settings:
                    allowed_settings_list.append(allowed_setting.value)
                settings_dict[setting_name] = allowed_settings_list
            else:
                settings_dict[setting_name] = ''
        return settings_dict

    def get_user_settings(self, user_id):
        user_settings_dict = {}

        user_settings = self._dao.list_where(
            where_clause="userId = %s",
            clazz=AvlanUserSettingStorage,
            arg_list=[user_id]
        )

        for user_setting in user_settings:
            setting = self._dao.load(
                clazz=AvlanSettingStorage,
                object_id=user_setting.settingId,
            )

            setting_name = setting.name
            if user_setting.allowedSettingId:
                allowed_setting = self._dao.load(
                    clazz=AvlanAllowedSettingStorage,
                    object_id=user_setting.allowedSettingId,
                )
                setting_value = allowed_setting.value
            else:
                setting_value = user_setting.value

            user_settings_dict[setting_name] = setting_value

        return user_settings_dict
