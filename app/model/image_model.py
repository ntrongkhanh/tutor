from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=True)
    data = db.Column(db.LargeBinary, nullable=True)
    user = relationship("User", uselist=False, back_populates="avatar")

    tutor_id = db.Column(db.Integer, ForeignKey('tutor.id'))
    tutor = relationship("Tutor", back_populates="images")
