from app import db


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    description1 = db.Column(db.String(200))

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

