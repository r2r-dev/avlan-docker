class AvlanInterfaceStorage(object):

    TABLE_ID = "id"
    SQL_TABLE = "Interface"
    SQL_ORDERBY = "T.id"

    def __init__(self):
        self.id = None
        self.nodeId = None
        self.peerNodeId = None
        self.peerIfaceId = None
        self.ifaceIndex = None
        self.mac = None
