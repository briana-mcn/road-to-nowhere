from flask import request

from road_to_nowhere.exceptions import RequestValidationError


def get_request_model(request_model, expected_params=None):
    result = {}

    if expected_params:
        for param in expected_params:
            if param not in request.args:
                raise RequestValidationError('Expected params not provided')
            result.update({param: request.args.get(param)})

    return request_model(**result)


def get_post_request_model(request_model, expected_keys=None):
    result = {}

    if expected_keys:
        request_body = request.get_json()

        for key in expected_keys:
            if key not in request_body.keys():
                raise RequestValidationError('Expected request keys not provided')
            else:
                result.update({key: request_body.get(key)})

    return request_model(**result)


def register_blueprints(flask_app, blueprints):
    for blueprint in blueprints:
        flask_app.register_blueprint(blueprint)
