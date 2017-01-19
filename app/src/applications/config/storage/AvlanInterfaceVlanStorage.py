class AvlanInterfaceVlanStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "InterfaceVlan"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.ifaceId = None
        self.vlanId = None
        self.pvid = None
