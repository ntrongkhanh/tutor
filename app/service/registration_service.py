import uuid
from datetime import datetime
from operator import or_

from sqlalchemy import desc

from app import db
from app.mail import mail
from app.model.class_model import Class
from app.model.model_enum import RegistrationStatus, PostStatus
from app.model.post_model import Post
from app.model.registration_model import Registration
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object


def create(args, author_id, post_id):
    author = User.query.get(author_id)
    if not author:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    post = Post.query.get(post_id)
    if not post:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
    if not post.is_tutor and not author.is_tutor:
        return response_object(status=False, message=response_message.USER_ARE_NOT_TUTOR), 403
    if post.user_id == author_id:
        return response_object(status=False, message=response_message.INTERNAL_SERVER_ERROR_500), 500

    check_registration = Registration.query.filter(Registration.post_id == post.id,
                                                   Registration.author_id == author_id,
                                                   Registration.status != RegistrationStatus.CANCEL).first()
    if check_registration:
        return response_object(status=False, message=response_message.INVITATION_ALREADY_EXISTS), 409

    registration = Registration(
        post_id=post_id,
        content=args['content'],
        contact=args['contact'],
        approved_user_id=post.user_id,
        author_id=author_id
    )
    db.session.add(registration)
    db.session.flush()
    try:
        if post.is_tutor:
            send_mail_register_to_study(registration, post.user.email)
        else:
            send_mail_register_to_teach(registration, post.user.email)
    except:
        pass
    db.session.commit()

    return response_object(), 201


def update():
    pass


def get_by_id(user_id, registration_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404

    registration = Registration.query.get(registration_id)
    if registration.approved_user_id != user_id and registration.author_id != user_id:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401
    if registration.approved_user_id == user_id:
        registration.is_read_by_approved_user = True
        db.session.commit()
    data = registration.to_json()

    return response_object(data=data), 200


def cancel(user_id, registration_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404

    registration = Registration.query.filter(Registration.id == registration_id,
                                             Registration.status == RegistrationStatus.PENDING).first()
    if not registration:
        return response_object(status=False, message=response_message.NOT_FOUND_404), 404

    if registration.author_id != user_id:
        return response_object(status=False, message=response_message.UNAUTHORIZED_401), 401

    registration.status = RegistrationStatus.CANCEL
    registration.updated_date = datetime.now()
    db.session.commit()

    return response_object(), 200


"""
    filter_request.add_argument("post_id", type=int, location="args", required=True)
    filter_request.add_argument("is_looking_for_tutor", type=bool, location="args", required=True)
    filter_request.add_argument("user_id", type=int, location="args", required=True)
    filter_request.add_argument("author_id", type=int, location="args", required=True)
    filter_request.add_argument("page", type=int, location="args", required=False, default=app.config['DEFAULT_PAGE'])
    filter_request.add_argument("page_size", type=int, location="args", required=False,
                                default=app.config['DEFAULT_PAGE_SIZE'])

                                page = args['page']
    page_size = args['page_size']
    rates = Rate.query.filter(Rate.user_id == user_id) \
        .order_by(desc(Rate.updated_date)) \
        .paginate(page, page_size, error_out=False)
"""


def get_wait_list(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    registrations = Registration.query.filter(Registration.approved_user_id == user_id,
                                              Registration.status == RegistrationStatus.PENDING) \
        .order_by(desc(Registration.created_date)) \
        .paginate(page, page_size, error_out=False)

    return response_object(data=[registration.to_json_with_read() for registration in registrations.items],
                           pagination={'total': registrations.total, 'page': registrations.page}), 200


def registered_list(args, user_id):
    page = args['page']
    page_size = args['page_size']

    status = args['status']
    if status not in RegistrationStatus._value2member_map_:
        status = None

    registrations = Registration.query.filter(Registration.author_id == user_id,
                                              or_(Registration.status == status, status is None)) \
        .order_by(desc(Registration.created_date)) \
        .paginate(page, page_size, error_out=False)
    return response_object(data=[r.to_json() for r in registrations.items],
                           pagination={'total': registrations.total, 'page': registrations.page}), 200


def taught_list(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    # posts = Post.query.filter(Post.class_.has(Class.teacher_id == user_id)) \
    #     .order_by(desc(Class.created_date)).paginate(
    #     page, page_size, error_out=False)
    classes = Class.query.filter(Class.teacher_id == user_id) \
        .order_by(desc(Class.created_date)) \
        .paginate(page, page_size, error_out=False)
    return response_object(data=[class_.to_json() for class_ in classes.items],
                           pagination={'total': classes.total, 'page': classes.page}), 200


def class_list(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    # posts = Post.query.filter(Post.class_.has(Class.teacher_id == user_id)) \
    #     .order_by(desc(Class.created_date)).paginate(
    #     page, page_size, error_out=False)
    classes = Class.query.filter(or_(Class.teacher_id == user_id, Class.student_id == user_id)) \
        .order_by(desc(Class.created_date)) \
        .paginate(page, page_size, error_out=False)
    return response_object(data=[class_.to_json() for class_ in classes.items],
                           pagination={'total': classes.total, 'page': classes.page}), 200


def studied_list(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    # posts = Post.query.filter(Post.class_.has(Class.teacher_id == user_id)) \
    #     .order_by(desc(Class.created_date)).paginate(
    #     page, page_size, error_out=False)
    classes = Class.query.filter(Class.student_id == user_id) \
        .order_by(desc(Class.created_date)) \
        .paginate(page, page_size, error_out=False)
    return response_object(data=[class_.to_json() for class_ in classes.items],
                           pagination={'total': classes.total, 'page': classes.page}), 200


def decline(user_id, registration_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    registration = Registration.query.get(registration_id)
    if not registration:
        return response_object(status=False, message=response_message.REGISTRATION_NOT_FOUND), 404

    if registration.approved_user_id != user_id:
        return response_object(status=False, message=response_message.INTERNAL_SERVER_ERROR_500), 500

    registration.status = RegistrationStatus.DECLINED
    registration.updated_date = datetime.now()
    db.session.commit()
    return response_object(), 200


def accept(user_id, registration_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    registration = Registration.query.get(registration_id)
    if registration.status != RegistrationStatus.PENDING:
        return response_object(status=False, message=response_message.INTERNAL_SERVER_ERROR_500), 500

    if not registration:
        return response_object(status=False, message=response_message.REGISTRATION_NOT_FOUND), 404
    if registration.approved_user_id != user_id:
        return response_object(status=False, message=response_message.INTERNAL_SERVER_ERROR_500), 500

    post = registration.post
    user_is_teacher = False

    if registration.approved_user_id == user_id and post.user_id == user_id and post.is_tutor:
        user_is_teacher = True
    elif registration.approved_user_id == user_id and post.user_id != user_id and not post.is_tutor:
        user_is_teacher = True
    elif registration.approved_user_id == user_id and post.user_id == user_id and not post.is_tutor:
        user_is_teacher = False

    class_ = Class(
        post_id=registration.post_id,
        teacher_id=user_id if user_is_teacher else registration.author_id,
        student_id=registration.author_id if user_is_teacher else user_id
    )

    registration.status = RegistrationStatus.ACCEPTED
    registration.updated_date = datetime.now()
    p = Post.query.get(registration.post_id)
    p.status = PostStatus.CLOSED
    db.session.add(class_)
    db.session.commit()
    return response_object(), 200


def invite(args, author_id):
    invited_user = User.query.get(args['invited_user_id'])
    if not invited_user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404

    post = Post(
        is_tutor=False,
        public_id='BD' + str(uuid.uuid4())[:6].upper(),
        title=args['title'],
        description=args['description'],
        city_address=args['city_address'],
        district_address=args['district_address'],
        detailed_address=args['detailed_address'],
        latitude=args['latitude'],
        longitude=args['longitude'],
        subject=args['subject'],
        class_type=args['class_type'],
        other_information=args['other_information'],
        fee=args['fee'],
        # schedule=args['schedule'],
        number_of_sessions=args['number_of_sessions'],
        require=args['require'],
        contact=args['contact'],
        form_of_teaching=args['form_of_teaching'],
        user_id=author_id,
        status=PostStatus.CLOSED
    )

    db.session.add(post)
    db.session.flush()

    registration = Registration(
        post_id=post.id,
        contact=args['contact'],
        content=args['content'],
        approved_user_id=args['invited_user_id'],
        author_id=author_id
    )
    db.session.add(registration)
    db.session.flush()
    send_mail_invite(registration, invited_user.email)
    db.session.commit()

    return response_object(), 201


def send_mail_register_to_study(registration, receiver_mail):
    link = f'http://localhost:3000/registration-post/{registration.id}'
    content = 'Có người đăng ký học lớp học của bạn:' + link
    mail.send_mail_without_template(receiver_mail, '[Tutor Online] Đăng ký lớp', content=content)

    return True


def send_mail_register_to_teach(registration, receiver_mail):
    link = f'http://localhost:3000/registration-post/{registration.id}'
    content = 'Có người đăng ký dạy lớp học của bạn:' + link
    mail.send_mail_without_template(receiver_mail, '[Tutor Online]Đăng ký dạy', content=content)

    return True


def send_mail_invite(registration, receiver_mail):
    link = f'http://localhost:3000/registration-post/{registration.id}'
    content = 'Có người mời bạn làm gia sư:' + link
    mail.send_mail_without_template(receiver_mail, '[Tutor online] Mời dạy học', content=content)

    return True
