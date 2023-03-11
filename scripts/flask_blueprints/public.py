import os
from flask import Blueprint, jsonify, current_app, request

public = Blueprint('public', __name__)

# /api/0/health
@public.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': f'This is from the public blueprint: {os.path.realpath(__file__)}'})

@public.route('/test', methods = ["GET", "POST"])
def test(**kwangs):
    print(kwangs)

    result_values = dict(request.values)
    print(result_values)

    try:
        result_json = request.json
    except:
        result_json = {}
    print(result_json)

    try:
        result_headers = request.headers
    except:
        result_headers = {}
    print(result_headers)

    result = {**result_values, **result_json, **kwangs, **result_headers}
    return jsonify(result)

@public.route('/login', methods=["POST"])
def login():
    # username = request.json.get('username')
    # password = request.json.get('password')
    return jsonify({'message': 'login endpoint', "status": 200}), 200

