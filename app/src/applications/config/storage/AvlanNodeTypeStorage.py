class AvlanNodeTypeStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "NodeType"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.type = None
