import enum


class DataSetCategories(enum.Enum):

    organic = 'organic'
    recycling = 'recycling'
    domestic = 'domestic'
    food = 'food'
    construction = 'construction'

    @classmethod
    def get_status_by_name(cls, name):
        return cls.__members__[name].value

    @classmethod
    def __values__(cls):
        return [member.value for member in cls]

    """Retrieve all statuses of this Enum, as a dict"""
    @classmethod
    def to_dict(cls):
        ret = {}
        for status in list(cls):
            ret[status._name_] = status._value_
        return ret
