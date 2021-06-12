import uuid
from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from sqlalchemy import desc

from app import db
from app.dto.registration_dto import RegistrationDto
from app.model.class_model import Class
from app.model.model_enum import RegistrationStatus, PostStatus
from app.model.post_model import Post
from app.model.registration_model import Registration
from app.model.user_model import User
from app.util import response_message
from app.util.api_response import response_object
from app.util.auth_parser_util import get_auth_required_parser

api = RegistrationDto.api

_create_request = RegistrationDto.create_request
# _update_request = RegistrationDto.update_request
_filter_request = RegistrationDto.filter_request
_message_response = RegistrationDto.message_response


@api.route('')
class CreateRegistrationController(Resource):
    @api.doc('create regis')
    @api.expect(_create_request, validate=True)
    @jwt_required()
    def post(self):
        """ đăng ký, ghi danh học/ dạy 1 bài post """
        args = _create_request.parse_args()
        user_id = get_jwt_identity()['user_id']
        return create(args, user_id)


@api.route('/<registration_id>')
class RegistrationController(Resource):
    # @api.doc('update registration')
    # @api.expect(_create_request, validate=True)
    #  
    # @jwt_required()
    # def put(self):
    #     return update()

    @api.doc('get by id registration')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    def get(self, registration_id):
        """ get by id bài đăng ký """
        user_id = get_jwt_identity()['user_id']

        return get_by_id(user_id, registration_id)


@api.route('/cancel/<registration_id>')
class RegistrationController(Resource):
    @api.doc('cancel registration')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    def get(self, registration_id):
        """ Người đăng ký hủy cái đăng ký (chưa đc duyệt) """
        user_id = get_jwt_identity()['user_id']

        return cancel(user_id, registration_id)


@api.route('/wait')
class WaitRegistrationController(Resource):
    @api.doc('Wait Regis list')
    @api.expect(_filter_request, validate=True)
    @jwt_required()
    def get(self):
        """danh sách các đăng ký chờ mình duyệt (từ chối hay chấp nhận)"""
        args = _filter_request.parse_args()
        user_id = get_jwt_identity()['user_id']

        return get_wait_list(args, user_id)


@api.route('/registered')
class RegisteredController(Resource):
    @api.doc('Registered list')
    @api.expect(_filter_request, validate=True)
    @jwt_required()
    def get(self):
        """ Danh sách mình đã đăng ký (đăng ký chờ duyệt, chưa học)  """
        args = _filter_request.parse_args()
        user_id = get_jwt_identity()['user_id']
        return registered_list(args, user_id)


@api.route('/taught')
class PostTaughtListController(Resource):
    @api.doc('Taught list')
    @api.expect(_filter_request, validate=True)
    @jwt_required()
    def get(self):
        """ Danh sách mình đã dạy"""
        args = _filter_request.parse_args()
        user_id = get_jwt_identity()['user_id']
        return taught_list(args, user_id)


@api.route('/studied')
class PostStudiedListController(Resource):
    @api.doc('Studied list')
    @api.expect(_filter_request, validate=True)
    @jwt_required()
    def get(self):
        """ Danh sách mình đã học """
        args = _filter_request.parse_args()
        user_id = get_jwt_identity()['user_id']
        return studied_list(args, user_id)


@api.route('/decline/<registration_id>')
class DeclineController(Resource):
    @api.doc('decline list')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    def post(self, registration_id):
        user_id = get_jwt_identity()['user_id']

        return decline(user_id, registration_id)


@api.route('/accept/<registration_id>')
class AcceptController(Resource):
    @api.doc('accept list')
    @api.expect(get_auth_required_parser(api), validate=True)
    @jwt_required()
    def post(self, registration_id):
        user_id = get_jwt_identity()['user_id']

        return accept(user_id, registration_id)


_invite_request = RegistrationDto.invite_request


@api.route('/invite-tutor')
class InviteTutorController(Resource):
    @api.doc('invite')
    @api.expect(_invite_request, validate=True)
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()['user_id']
        args = _invite_request.parse_args()
        return invite(args, user_id)


def create(args, author_id):
    author = User.query.get(author_id)
    if not author:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    post = Post.query.get(args['post_id'])
    if not post:
        return response_object(status=False, message=response_message.POST_NOT_FOUND), 404
    if not post.is_tutor and not author.is_tutor:
        return response_object(status=False, message=response_message.USER_ARE_NOT_TUTOR), 403
    if post.user_id == author_id:
        return response_object(status=False, message=response_message.INTERNAL_SERVER_ERROR_500), 500

    check_registration = Registration.query.filter(Registration.post_id == post.id).first()
    if check_registration:
        return response_object(status=False, message=response_message.INVITATION_ALREADY_EXISTS), 409

    registration = Registration(
        post_id=args['post_id'],
        approved_user_id=post.user_id,
        author_id=author_id
    )
    db.session.add(registration)
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

    data = registration.to_json()

    return response_object(data=data), 200


def cancel(user_id, registration_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404

    registration = Registration.query.get(registration_id)
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

    return response_object(data=[registration.to_json() for registration in registrations.items],
                           pagination={'total': registrations.total, 'page': registrations.page}), 200


def registered_list(args, user_id):
    user = User.query.get(user_id)
    if not user:
        return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
    page = args['page']
    page_size = args['page_size']
    registrations = Registration.query.filter(Registration.author_id == user_id) \
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


#
# def taught_list(args, user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
#     page = args['page']
#     page_size = args['page_size']
#     registrations = Registration.query.filter(
#         or_(
#             and_(
#                 and_(Registration.post.has(Post.user_id == user_id), Registration.post.has(Post.is_tutor)),
#                 Registration.approved_user_id == user_id
#             ),
#             or_(
#                 and_(
#                     and_(Registration.post.has(Post.user_id != user_id), Registration.post.has(Post.is_tutor==False)),
#                     Registration.approved_user_id == user_id
#                 ),
#                 and_(
#                     and_(Registration.post.has(Post.user_id != user_id), Registration.post.has(Post.is_tutor==True)),
#                     Registration.approved_user_id != user_id
#                 )
#             )
#         ),
#         Registration.status == RegistrationStatus.ACCEPTED) \
#         .order_by(desc(Registration.created_date)) \
#         .paginate(page, page_size, error_out=False)
#
#     return response_object(data=[registration.to_json() for registration in registrations.items],
#                            pagination={'total': registrations.total, 'page': registrations.page}), 200
#
#
# def studied_list(args, user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return response_object(status=False, message=response_message.USER_NOT_FOUND), 404
#     page = args['page']
#     page_size = args['page_size']
#     registrations = Registration.query.filter(
#         or_(
#             and_(
#                 and_(Registration.post.has(Post.user_id == user_id), Registration.post.has(Post.is_tutor==False)),
#                 Registration.approved_user_id == user_id
#             ),
#             or_(
#                 and_(
#                     and_(Registration.post.has(Post.user_id != user_id), Registration.post.has(Post.is_tutor)),
#                     Registration.approved_user_id != user_id
#                 ),
#                 and_(
#                     and_(Registration.post.has(Post.user_id == user_id), Registration.post.has( Post.is_tutor==False)),
#                     Registration.approved_user_id != user_id
#                 )
#             )
#         ),
#         Registration.status == RegistrationStatus.ACCEPTED) \
#         .order_by(desc(Registration.created_date)) \
#         .paginate(page, page_size, error_out=False)
#
#     return response_object(data=[registration.to_json() for registration in registrations.items],
#                            pagination={'total': registrations.total, 'page': registrations.page}), 200


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
    # elif registration.approved_user_id != user_id and post.user_id != user_id and not post.is_tutor:
    #     user_is_teacher = True
    elif registration.approved_user_id == user_id and post.user_id == user_id and not post.is_tutor:
        user_is_teacher = False
    # elif registration.approved_user_id != user_id and post.user_id != user_id and post.is_tutor:
    #     user_is_teacher = False
    # elif registration.approved_user_id != user_id and post.user_id == user_id and not post.is_tutor:
    #     user_is_teacher = False

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
    post = Post(
        is_tutor=False,
        public_id='BD' + str(uuid.uuid4())[:6].upper(),
        title=args['title'],
        description=args['description'],
        city_address=args['city_address'],
        district_address=args['district_address'],
        detailed_address=args['detailed_address'],
        point_address=args['point_address'],
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
        approved_user_id=args['invited_user_id'],
        author_id=author_id
    )
    db.session.add(registration)
    db.session.commit()

    return response_object(), 201
