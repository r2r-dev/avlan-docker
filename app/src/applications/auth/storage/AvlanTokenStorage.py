class AvlanTokenStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "Token"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.value = None
        self.expirationDate = None
