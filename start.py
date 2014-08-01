import os, requests
from flask import Flask, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper
app = Flask(__name__)



# app.config.update(dict(
#     DEBUG = False,
#     TRANSLINK_API_URL = 'http://api.translink.ca/rttiapi/v1/',
#     TRANSLINK_API_KEY = 'Y0SgOFBTcRPW2nkOx9gA',
# ))

url = 'http://api.translink.ca/rttiapi/v1/'
api = {'apikey':'Y0SgOFBTcRPW2nkOx9gA'}
header = {'content-type':'application/JSON', 'accept':'application/JSON'}
port = int(os.environ.get('PORT', 5000))

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Content-Type'] = 'application/json'
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/')
@crossdomain(origin='*')
def index():
    return 'Hello world!'

@app.route('/api/stop/<stop_id>')
@crossdomain(origin='*')
def stop(stop_id):
    r = requests.get(url + 'stops/' + stop_id, params = api, headers = header)
    return r.text

@app.route('/api/stop/<stop_id>/<route_id>')
@crossdomain(origin='*')
def stop_route(stop_id, route_id):
    stop_route_api = api
    stop_route_api['route'] = route_id
    r = requests.get(url + 'stops/' + stop_id, params = stop_route_api, headers = header)
    return r.text

@app.route('/api/estimate/<stop_id>')
@crossdomain(origin='*')
def estimate(stop_id):
    r = requests.get(url + 'stops/' + stop_id + '/estimates', params = api, headers = header)
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
