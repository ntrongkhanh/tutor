from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    # user = relationship("User", backref="search_history", lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content
        }
