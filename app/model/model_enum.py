import enum


class TutorStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class PostStatus(enum.Enum):
    OPENING = "OPENING"
    CLOSED = "CLOSED"
