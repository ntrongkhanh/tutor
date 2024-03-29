import datetime
import random
import re
import string
from operator import or_, and_

from sqlalchemy import func

import app.util.response_message as message
from app import db, app
from app.mail import mail
from app.model.class_model import Class
from app.model.code_model import Code
from app.model.image_model import Image
from app.model.rate_model import Rate
from app.model.user_model import User
from app.util.api_response import response_object


def create_user(args):
    valid = validate_email_and_password(args['email'], args['password'])
    if not isinstance(valid, bool):
        return valid

    if User.query.filter(func.lower(User.email) == func.lower(args['email'])).first():
        return response_object(status=False, message=message.CONFLICT_409), 409
    print(args['email'])
    # image = Image(description='Avatar of ' + args['email'], data=None)
    # db.session.add(image)
    # db.session.flush()
    user = User(
        email=args['email'],
        password=args['password'],
        first_name=args['first_name'],
        last_name=args['last_name'],
        sex=args['sex']
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
        return response_object(status=False, data=str(e)), 500

    return response_object(), 201


def update_user(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=message.USER_NOT_FOUND), 404

    user.sex = args['sex'] if args['sex'] else user.sex
    user.last_name = args['last_name'] if args['last_name'] else user.last_name
    user.first_name = args['first_name'] if args['first_name'] else user.first_name
    # user.birthday = args['birthday']
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
    return response_object(data=user.to_json_tutor()), 200


def update_avatar(file, user_id):
    user = User.query.get(user_id)

    data = file.read()

    if not user:
        return response_object(status=False, message=message.USER_NOT_FOUND), 404
    if not user.avatar_id:
        image = Image(description='Avatar of ' + user.email, data=data)
        db.session.add(image)
        db.session.flush()
        user.avatar_id = image.id
    else:
        image = Image.query.get(user.avatar_id)
        image.data = data
        image.link = None
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
        code=''.join(random.choice(string.ascii_letters) for i in range(8))
    )

    db.session.add(reset_code)
    db.session.commit()

    if send_mail_reset_password(reset_code):
        return response_object(), 200
    else:
        return response_object(status=False, message=message.FAILED), 500


def reset_password(args, password):
    if not validate_password(password):
        return response_object(status=False, message=message.INVALID_PASSWORD), 400
    reset_code = Code.query.filter_by(email=args['email']).first()
    if not reset_code:
        return response_object(status=False, message=message.NOT_FOUND_404), 404
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
    content = 'Vui lòng nhấn vào link để kích hoạt tài khoản: ' + link_active
    mail.send_mail_without_template(active_code.email, '[Tutor Online] Kích hoạt tài khoản', content=content)

    return True


def active_user(args):
    active_code = Code.query.filter(Code.email == args['email']).first()
    if not active_code:
        return response_object(status=False, message=message.NOT_FOUND_404), 404
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
    if not validate_password(args['new_password']):
        return response_object(status=False, message=message.INVALID_PASSWORD), 400
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
        # link_reset = app.config['SERVER_ADDRESS'] + f'/api/user/reset/?email={reset_code.email}&code={reset_code.code}'
        content = 'Mã reset mật khẩu của bạn là: ' + reset_code.code
        mail.send_mail_without_template(reset_code.email, '[Tutor Online]Reset mật khẩu', content=content)
    except:
        return False
    return True


def validate_email_and_password(email, password):
    if not validate_email(email):
        return response_object(status=False, message=message.INVALID_EMAIL), 400
    if not validate_password(password):
        return response_object(status=False, message=message.INVALID_PASSWORD), 400

    return True


def validate_password(password):
    if len(password) < app.config['MIN_PASSWORD_CHARACTERS']:
        return False
    return True


def validate_email(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if not re.search(regex, email):
        return False
    return True


def get_by_id(user_id, author_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=message.USER_NOT_FOUND), 404
    classes = Class.query.filter(
        or_(
            and_(Class.student_id == author_id, Class.teacher_id == user_id),
            and_(Class.teacher_id == author_id, Class.student_id == user_id)
        )).all()
    rate = Rate.query.filter(Rate.user_id == user_id, Rate.author_id == author_id).all()

    if len(classes) == 0:
        can_rate = False
    elif len(classes) > len(rate):
        can_rate = True
    else:
        can_rate = False
    if user.is_tutor:
        data = user.to_json_tutor()
    else:
        data = user.to_json()

    data['can_rate'] = can_rate

    return response_object(data=data), 200
