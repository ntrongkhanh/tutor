from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class SearchData(db.Model):
    __tablename__ = 'search_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=True, unique=True)

    content = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="search_data")
