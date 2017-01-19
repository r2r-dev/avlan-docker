from src.applications.base.view.AvlanBaseView import AvlanBaseView


class AvlanTopologyMapView(AvlanBaseView):
    __template = 'webroot/html/AvlanTopologyMapTemplate.tmpl'

    def __init__(self, translation=None):
        AvlanBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.title = "Topology"
