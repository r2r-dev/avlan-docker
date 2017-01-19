from src.utils.crawler.mediator.AvlanCrawlerHpCurveMediator import\
    AvlanCrawlerHpCurveMediator
from src.utils.crawler.mediator.AvlanCrawlerEdgeCoreMediator import \
    AvlanCrawlerEdgeCoreMediator


class AvlanCrawlerMediatorFactory(object):
    __node_types = {
        'hp_procurve': AvlanCrawlerHpCurveMediator,
        'edgecore': AvlanCrawlerEdgeCoreMediator,
    }

    @classmethod
    def factory(cls, type, *args, **kwargs):
        try:
            return cls.__node_types[type](
                *args,
                **kwargs
            )
        except KeyError, e:
            raise UnknownMeditatorTypeException(e)


class UnknownMeditatorTypeException(Exception):
    def __init___(self, type):
        Exception.__init__(
            self,
            "Unknown mediator type {0:s}".format(type)
        )
        self.type = type
