import os, requests
from flask import Flask, request, session, g
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

@app.route('/')
def indexhandler():
    return 'Hello world!'

@app.route('/api/stop/<stop_id>')
def stop(stop_id):
    r = requests.get(url + 'stops/' + stop_id, params = api, headers = header)
    return r.text

@app.route('/api/stop/<stop_id>/<route_id>')
def stop_route(stop_id, route_id):
    stop_route_api = api
    stop_route_api['route'] = route_id
    r = requests.get(url + 'stops/' + stop_id, params = stop_route_api, headers = header)
    return r.text

@app.route('/api/estimate/<stop_id>')
def estimate(stop_id):
    r = requests.get(url + 'stops/' + stop_id + '/estimates', params = api, headers = header)
    return r.text
0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)