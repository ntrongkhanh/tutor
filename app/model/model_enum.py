import enum


class TutorStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PostStatus(enum.Enum):
    OPENING = "OPENING"
    CLOSED = "CLOSED"


class RegistrationStatus(enum.Enum):
    PENDING = "PENDING"
    DECLINED = "DECLINED"
    ACCEPTED = "ACCEPTED"
