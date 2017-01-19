class AvlanNodeStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "Node"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.ipAddress = None
        self.sshPort = None
        self.sshUsername = None
        self.sshPassword = None
