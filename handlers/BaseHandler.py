
import json
from urllib import parse as urlparse
import traceback
import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, handler):
        self.handler = handler

    def get(self, *args, **kwargs):
        self.handle_request(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        self.handle_request(*args, **kwargs)

    def handle_request(self, *args, **kwargs):
        data = kwargs
        req = self.request
        parse_res = urlparse.urlparse(req.uri)
        path = parse_res.path

        for arg, val in urlparse.parse_qs(parse_res.query).items():
            data[arg] = val[0]

        if req.body:
            body_args = json.loads(req.body)
            data.update(body_args)

        method = path.split('/')[-1]
        if not method.startswith('_') and hasattr(self, method):
            try:
                resp = getattr(self, method)(data)
            except Exception as e:
                resp = self.internal_server_error_response(str(e) + "\n" + traceback.format_exc())
        else:
            resp = self.unknown_api_response()

        self.set_status(resp['http_code'])
        self.write(resp['body'])
        self.finish()

    def success_responce(self, data):
        return {"http_code": 200, "body": data}
    
    def failure_responce(self, code, data):
        return {"http_code": code, "body": data}

    def unknown_api_response(self):
        
        return {
            "http_code": 404, 
            "body": "unknown api"
        }

    def internal_server_error_response(self, e):
        return {
            "http_code": 500,
            "body": str(e)
        } 

