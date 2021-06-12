import enum


class TutorStatus(enum.Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class PostStatus(enum.Enum):
    OPENING = 'OPENING'
    CLOSED = 'CLOSED'


class RegistrationStatus(enum.Enum):
    PENDING = 'PENDING'
    CANCEL = 'CANCEL'
    DECLINED = 'DECLINED'
    ACCEPTED = 'ACCEPTED'


def convert_keys(obj, convert=str):
    if isinstance(obj, list):
        return [convert_keys(i, convert) for i in obj]
    if not isinstance(obj, dict):
        return obj
    return {convert(k): convert_keys(v, convert) for k, v in obj.items()}


def enum_to_json(key, type):
    if isinstance(key, type):
        return key.name
    return str(key)

# def enum_names(key):
#     if isinstance(key, TestEnum):
#         return key.name
#     return str(key)
