class AvlanSettingStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "Setting"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.name = None
