from datetime import datetime

import response_message


def response_object(status=True, message=response_message.SUCCESS, data=[], pagination=None):
    if not pagination:
        return {
            'status': status,
            'message': message,
            'data': data,
        }
    else:
        return {
            'status': status,
            'message': message,
            'data': data,
            'pagination': pagination
        }


def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
