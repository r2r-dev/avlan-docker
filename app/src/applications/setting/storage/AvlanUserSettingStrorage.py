class AvlanUserSettingStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "UserSetting"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.userId = None
        self.settingId = None
        self.allowedSettingId = None
        self.value = None
