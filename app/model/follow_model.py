from app import db


class Follow(db.Model):
    __tablename__ = 'follow'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)

# follow_table = db.Table('follow', db.Model.metadata,
#                         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#                         db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
#                         )