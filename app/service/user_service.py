import datetime
import random
import string

import app.util.response_message as message
from app import db, app
from app.mail import mail
from app.model.code import Code
from app.model.image_model import Image
from app.model.user_model import User
from app.util.api_response import response_object


def create_user(args, file):
    if User.query.filter(User.email == args['email']).first():
        return response_object(status=False, message=message.EMAIL_ALREADY_EXISTS), 400
    data = file.read()
    image = Image(description='Avatar of ' + args['email'], data=data if data else None)
    db.session.add(image)
    db.session.flush()

    user = User(
        email=args['email'],
        password=args['password'],
        first_name=args['first_name'],
        last_name=args['last_name'],
        birthday=args['birthday'],
        # sex=True if args['sex'] == 'true' else False,
        sex=args['sex'],
        avatar_id=image.id
    )
    active_code = Code(
        email=user.email,
        code=''.join(random.choice(string.ascii_letters) for i in range(20))
    )

    db.session.add(user)
    db.session.add(active_code)

    try:

        if not send_mail_active_user(active_code=active_code):
            return response_object(status=False, message=message.CREATE_FAILED), 500

        db.session.commit()

    except Exception as e:
        print(e)
        return response_object(status=False, message=message.CREATE_FAILED), 500
    return response_object(), 201


def update_user(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=message.USER_NOT_FOUND), 404
    user.sex = args['sex']
    user.last_name = args['last_name']
    user.first_name = args['first_name']
    user.birthday = args['birthday']
    user.updated_date = datetime.datetime.now()

    try:
        db.session.commit()
    except:
        return response_object(status=False, message=message.UPDATE_FAILED), 500

    return response_object(), 200


def get_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=message.USER_NOT_FOUND), 404
    return response_object(data=user.to_json()), 200


def update_avatar(file, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=message.USER_NOT_FOUND), 404
    image = Image.query.filter(Image.user == user).first()

    data = file.read()
    file_name = file.filename
    image.data = data
    image.description = file_name
    image.updated_date = datetime.datetime.now()
    db.session.commit()

    return response_object(), 200


def login(args):
    user = User.query.filter_by(email=args['email']).first()
    if not user:
        return response_object(status=False, message=message.USER_NOT_FOUND), 404
    if not user.verify_password(args['password']):
        return response_object(status=False, message=message.PASSWORD_WRONG), 401

    data = user.to_json()

    return response_object(data=data), 200


def forgot_password(email):
    reset_code = Code(
        email=email,
        code=''.join(random.choice(string.ascii_letters) for i in range(20))
    )
    db.session.add(reset_code)
    db.session.commit()
    if send_mail_reset_password(reset_code):
        return response_object(), 200
    else:
        return response_object(status=False, message=message.FAILED), 500


def reset_password(args, password):
    reset_code = Code.query.filter_by(email=args['email']).first()
    if not reset_code:
        return response_object(status=False, message=message.NOT_FOUND), 404
    if reset_code.code == args['code']:
        try:
            user = User.query.filter(User.email == reset_code.email).first()
            user.set_password(password)
            user.updated_date = datetime.datetime.now()
            db.session.delete(reset_code)
            db.session.commit()
        except:
            return response_object(status=False, message=message.RESET_FAILED), 500

    return response_object(), 200


def send_mail_active_user(active_code):
    link_active = app.config['SERVER_ADDRESS'] + f'/api/user/active/?email={active_code.email}&code={active_code.code}'
    content = 'Please click on the link to activate your account: ' + link_active
    mail.send_mail_without_template(active_code.email, 'Active account', content=content)

    return True


def active_user(args):
    active_code = Code.query.filter(Code.email == args['email']).first()
    if not active_code:
        return response_object(status=False, message=message.NOT_FOUND), 404
    if active_code.code == args['code']:
        try:
            user = User.query.filter(User.email == active_code.email).first()
            user.is_active = True
            db.session.delete(active_code)
            db.session.commit()
        except:
            return response_object(status=False, message=message.ACTIVE_FAILED), 500

    return response_object(), 200


def change_password(args, id_user):
    user = User.query.get(id_user)
    if not user:
        return response_object(status=False, message=message.USER_NOT_FOUND), 404
    if not user.verify_password(args['old_password']):
        return response_object(status=False, message=message.PASSWORD_WRONG), 401
    user.set_password(args['new_password'])
    user.updated_date = datetime.datetime.now()
    try:
        db.session.commit()
    except:
        return response_object(status=False, message=message.UPDATE_FAILED), 500
    return response_object(), 200


def send_mail_reset_password(reset_code):
    try:
        link_reset = app.config['SERVER_ADDRESS'] + f'/api/user/reset/?email={reset_code.email}&code={reset_code.code}'
        content = 'Please click on the link to reset your password: ' + link_reset
        mail.send_mail_without_template(reset_code.email, 'Reset password', content=content)
    except:
        return False
    return True


def test_send_mail():
    mail.send_mail_without_template(receiver='trongkhanhvip1@gmail.com', content='hello')
