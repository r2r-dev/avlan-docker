class AvlanUserStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "User"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.tokenId = None
