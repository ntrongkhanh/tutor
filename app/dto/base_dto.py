from flask_restx import fields, Model

base = Model('base', {
    'code': fields.Integer,
    'status': fields.Boolean,
    'message': fields.String
})
