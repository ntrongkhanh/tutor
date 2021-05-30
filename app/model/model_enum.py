import enum


class TutorStatus(enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


class PostStatus(enum.Enum):
    OPEN = "Open"
    CLOSED = "Closed"
