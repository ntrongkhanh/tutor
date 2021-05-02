from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False), #unique=True
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    sex = db.Column(db.Boolean, default=True, nullable=True)
    is_tutor = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    avatar_id = db.Column(db.Integer, ForeignKey('image.id'), nullable=True)

    avatar = relationship("Image", back_populates="user")
    posts = relationship("Post", back_populates="user")
    search_data = relationship("SearchData", back_populates="user")

    def to_json(self):
        return {
            'email': self.email,
            'password': self.password,
            'first_name': self.last_name,
            'last_name': self.last_name,
            'sex': self.sex,
        }
