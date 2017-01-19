class AvlanAllowedSettingStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "AllowedSetting"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.settingId = None
        self.value = None
        self.default_setting = None
