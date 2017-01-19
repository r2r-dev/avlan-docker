class AvlanVlanStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "Vlan"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.number = None
        self.nodeId = None
        self.name = None
