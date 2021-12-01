# import datetime
#
# from sqlalchemy import ForeignKey
#
# from app import db
# from app.util.api_response import date_to_json
#
#
# class SearchHistory(db.Model):
#     __tablename__ = 'search_history'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     content = db.Column(db.String(255), nullable=True)
#
#     user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
#     # user = relationship("User", backref="search_history", lazy=True)
#
#     created_date = db.Column(db.DateTime, nullable=True)
#
#     def __init__(self, content, user_id):
#         self.content = content
#         self.user_id = user_id
#         self.created_date = datetime.datetime.now()
#
#     def to_json(self):
#         return {
#             'id': self.id,
#             'content': self.content,
#             'created_date': date_to_json(self.created_date)
#         }
