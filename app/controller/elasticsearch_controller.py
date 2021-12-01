from flask_restx import Resource

from app import es
from app.dto.elasticsearch_dto import ElasticsearchDto
from app.model.post_model import Post
from app.model.schedule_model import Schedule
from app.model.user_model import User
from app.util import elasticsearch_index
from app.util.api_response import response_object

api = ElasticsearchDto.api


@api.route('/test')
class Test(Resource):
    def get(self):
        from app.controller.test import test1

        return test1()


@api.route('')
class ElasticsearchInitialization(Resource):
    def get(self):
        if es.ping():

            indices = [elasticsearch_index.TUTOR, elasticsearch_index.LOOKING_FOR_TUTOR_POST,
                       elasticsearch_index.LOOKING_FOR_STUDENT_POST]
            es.delete_by_query(index=indices, body={"query": {"match_all": {}}})

            tutors = User.query.filter(User.is_tutor, User.is_active).all()
            tutor_posts = Post.query.filter(Post.is_tutor == False, Post.is_active).all()
            student_posts = Post.query.filter(Post.is_tutor, Post.is_active).all()

            #           es = Elasticsearch('host-address:port')
            for tutor in tutors:
                body = {
                    'id': tutor.id,
                    'first_name': tutor.first_name,
                    'last_name': tutor.last_name,
                    'is_tutor': tutor.is_tutor,
                    'public_id': tutor.tutor.public_id,
                    'career': tutor.tutor.career,
                    'tutor_description': tutor.tutor.tutor_description,
                    'majors': tutor.tutor.majors,
                    'degree': tutor.tutor.degree,
                    'school': tutor.tutor.school,
                    'city_address': tutor.tutor.city_address,
                    'district_address': tutor.tutor.district_address,
                    'detailed_address': tutor.tutor.detailed_address,
                    'latitude': tutor.tutor.latitude,
                    'longitude': tutor.tutor.longitude,
                    'subject': tutor.tutor.subject,
                    'class_type': tutor.tutor.class_type
                }
                es.index(index=elasticsearch_index.TUTOR, id=body['id'], body=body)
            for post in tutor_posts:
                body = {
                    'id': post.id,
                    'public_id': post.public_id,
                    'title': post.title,
                    'description': post.description,
                    'city_address': post.city_address,
                    'district_address': post.district_address,
                    'detailed_address': post.detailed_address,

                    'latitude': post.latitude,
                    'longitude': post.longitude,

                    'subject': post.subject,
                    'class_type': post.class_type,
                    'fee': post.fee,
                    'number_of_sessions': post.number_of_sessions,
                    'require': post.require,
                    'contact': post.contact,
                    'form_of_teaching': post.form_of_teaching,
                    'schedules': Schedule.to_json_list(post.schedules)
                }
                es.index(index=elasticsearch_index.LOOKING_FOR_TUTOR_POST, id=body['id'], body=body)

            for post in student_posts:
                body = {
                    'id': post.id,
                    'public_id': post.public_id,
                    'title': post.title,
                    'description': post.description,
                    'city_address': post.city_address,
                    'district_address': post.district_address,
                    'detailed_address': post.detailed_address,
                    'latitude': post.latitude,
                    'longitude': post.longitude,
                    'subject': post.subject,
                    'class_type': post.class_type,
                    'fee': post.fee,
                    'number_of_sessions': post.number_of_sessions,
                    'require': post.require,
                    'contact': post.contact,
                    'form_of_teaching': post.form_of_teaching,
                    'schedules': Schedule.to_json_list(post.schedules)
                }
                es.index(index=elasticsearch_index.LOOKING_FOR_STUDENT_POST, id=body['id'], body=body)
            return 'ok'
        else:
            return 'Oops'


search = api.parser()
search.add_argument('key', type=str)


@api.route('/update')
class Update(Resource):
    def get(self):
        body = {
            'id': 1065,
            'first_name': "đã sửa",
            'last_name': "đã sửa",
            'is_tutor': 'true',
            'public_id': "đã sửa",
            'career': "đã sửa",
            'tutor_description': "đã sửa",
            'majors': "đã sửa",
            'degree': "đã sửa",
            'school': "đã sửa",
            'city_address': "đã sửa",
            'district_address': "đã sửa",
            'detailed_address': "đã sửa",

            'latitude': 0,
            'longitude': 0,

            # 'latitude': tutor.tutor.latitude,
            # 'longitude': tutor.tutor.longitude,
            'subject': "đã sửa",
            'class_type': "đã sửa"
        }
        es.index(index=elasticsearch_index.TUTOR, id=body['id'], body=body)


@api.route('/search')
class Search(Resource):
    @api.expect(search, validate=True)
    def get(self):
        args = search.parse_args()
        keyword = args['key']

#       es = Elasticsearch('host-address:port')
        body = {
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["field-1", "field-2", "field-3", "field-4", ]
                },
            },

        }
        res = es.search(index=elasticsearch_index.TUTOR, body=body)

        res_list = res['hits']['hits']

        id_list = [re['_id'] for re in res_list]

        posts = User.query.filter(User.id.in_(id_list)).all()
        # posts = User.query.filter(User.is_tutor).all()
        # data = []
        # for post in posts:
        #     data.append(f'{post.tutor.latitude} + {post.tutor.longitude}= {post.tutor.latitude + post.tutor.longitude}')

        return response_object(data=[post.to_json() for post in posts]), 200
