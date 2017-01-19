class AvlanConfigStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "Config"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.title = None
        self.active = None
