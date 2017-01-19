from src.applications.setting.storage.AvlanSettingStorage import (
    AvlanSettingStorage
)
from src.applications.setting.storage.AvlanAllowedSettingStorage import (
    AvlanAllowedSettingStorage
)
from src.applications.config.storage.AvlanNodeTypeStorage import (
    AvlanNodeTypeStorage
)

default_node_types = [
    {
        'type': 'edgecore',
    },
    {
        'type': 'hp_procurve',
    },
]

default_settings = [
    {
        'id': 1,
        'name': 'language',
    },
    {
        'id': 2,
        'name': 'color',
    },
    {
        'id': 3,
        'name': 'image',
    },
]

default_allowed_settings = [
    {
        'id': 1,
        'settingId': 1,
        'value': 'pl',
        'default_setting': 0,
    },
    {
        'id': 2,
        'settingId': 1,
        'value': 'en',
        'default_setting': 1,
    },
    {
        'id': 3,
        'settingId': 2,
        'value': 'dark',
        'default_setting': 1,
    },
    {
        'id': 4,
        'settingId': 2,
        'value': 'light',
        'default_setting': 0,
    }
]


def create_defaults():
    def fill_default_object(_clazz, object_templates):
        _dao_objects = []
        for object_template in object_templates:
            dao_object = _clazz()
            for key, value in object_template.iteritems():
                setattr(
                    dao_object,
                    key,
                    value,
                )
            _dao_objects += [dao_object]
        return _dao_objects

    dao_objects = []

    '''
    Order is important due to use of foreign key constrains.
    '''
    dao_objects += fill_default_object(
        AvlanSettingStorage,
        default_settings,
    )
    dao_objects += fill_default_object(
        AvlanAllowedSettingStorage,
        default_allowed_settings,
    )
    dao_objects += fill_default_object(
        AvlanNodeTypeStorage,
        default_node_types,
    )

    return dao_objects
