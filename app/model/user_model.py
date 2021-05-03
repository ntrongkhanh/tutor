from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    sex = db.Column(db.Boolean, default=True, nullable=True)
    is_tutor = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    avatar_id = db.Column(db.Integer, ForeignKey('image.id'), nullable=True)

    # avatar = relationship("Image", backref="user", lazy=True)
    posts = relationship("Post", backref="user", lazy=True)
    search_history = relationship("SearchHistory", backref="user", lazy=True)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.last_name,
            'last_name': self.last_name,
            'sex': self.sex,
            'is_tutor': self.is_tutor,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'avatar_id': self.avatar_id,
            'avatar': self.avatar
        }
