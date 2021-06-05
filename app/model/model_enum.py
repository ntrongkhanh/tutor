import enum
import json


class TutorStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PostStatus(enum.Enum):
    OPENING = "OPENING"
    CLOSED = "CLOSED"
#
# class EnumEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if type(obj) in TutorStatus.values():
#             return {"__enum__": str(obj)}
#         return json.JSONEncoder.default(self, obj)
#
# def as_enum(d):
#     if "__enum__" in d:
#         name, member = d["__enum__"].split(".")
#         return getattr(TutorStatus[name], member)
#     else:
#         return d