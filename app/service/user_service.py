from app import db
from app.model.user_model import User


def create_user(args):
    user = User(
        email='email',
        password='password',
        first_name='first_name',
        last_name='last_name',
        sex=True,
        is_tutor=False,
        is_admin=False,
        is_active=False,
        avatar_id=None
    )

    db.session.add(user)
    db.session.commit()

    data = user.to_json()
    return data
