import json
import importlib
from flask import Flask, request
from flask_restful import Resource, Api


def lambda_handler(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


app = Flask(__name__)
api = Api(app)


@app.route("/api/v1/hello")
def hello():
    return "Hello World!"


class RainforestCallback(Resource):
    def post(self):
        try:
            try:
                print(request.json)
                # db_id = get_db_object().save_request({"request": req})
                # err, error_code, req = Validator(req).validate_docusign_request()
                # if len(err) > 0:
                #     return Response(400, GENERIC_HEADER, err, None, None).prepare_http_response()

                run_process = load_module("v1", "rainforest_callback").run(request)
                # get_db_object().save_response(db_id, {"response": run_process})
                # return Response(201, GENERIC_HEADER, run_process, None, None).prepare_http_response()
            except Exception as exception:
                pass
                # exception = exception.__class__.__name__
                # if exception in Exception_object:
                #     code = Exception_object[exception]['code']
                #     message = Exception_object[exception]['message']
                #     return Response(code, GENERIC_HEADER, message, None, None).prepare_http_response()
                # Logger(request).error(exception)
                # return Response(500, GENERIC_HEADER, HTTP_ERROR.get('ACTION_FAILED_ERROR'), None, None) \
                #     .prepare_http_response()
        except Exception as e:
            raise e


api.add_resource(RainforestCallback, '/api/v1/rainforest_callback')


def load_module(version, module_name):
    module = importlib.import_module('service.' + version + '.' + module_name)
    provider_class = getattr(module, module_name.title())()
    return provider_class
