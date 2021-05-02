from app import db
from app.model.demo_model import Demo


def create_demo(args):
    demo = Demo(
        username=args['username'],
        password=args['password']
    )

    db.session.add(demo)
    db.session.commit()

    return demo
