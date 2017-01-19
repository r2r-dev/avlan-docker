from os import listdir
from os.path import (
    splitext,
    join,
)
from json import load
from src.conf import settings


class AvlanTranslator(object):
    def __init__(self):
        self.translations = {}
        self.active_translation = None
        translation_dir = settings.translation_dir

        for translation_file in listdir(translation_dir):
            translation_name = splitext(translation_file)[0]
            translation_path = join(
                translation_dir,
                translation_file,
            )
            with open(translation_path) as translation:
                self.translations[translation_name] = load(translation)

    def gettext(self, message):
        if self.active_translation is None:
            return message
        try:
            return self.translations[self.active_translation][message]
        except KeyError:
            return message

    def activate(self, translation):
        self.active_translation = translation

_trans = AvlanTranslator()

del AvlanTranslator


def gettext(message):
    return _trans.gettext(message)


def activate(translation):
    return _trans.activate(translation)
