from app import db


class Code(db.Model):
    __tablename__ = 'code'

    email = db.Column(db.String(255), nullable=False, primary_key=True)
    code = db.Column(db.String(255), nullable=False)
