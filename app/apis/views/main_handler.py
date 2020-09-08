"""app/apis/views/main_handler.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
from flask import Blueprint, jsonify, request

from app.apis.views.back_end_handler import handler as back_end_handler
from app.apis.views.front_end_handler import handler as front_end_handler
from app.common.utility import err_response

apis = Blueprint(name='raspi-streaming', import_name=__name__,
                 url_prefix='/raspi-streaming')


@apis.route('/healthcheck', methods=['GET'])
def healthcheck():
    """healthcheck
    """
    return jsonify({'status': 'healthy'}), 200


@apis.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    """api
    """
    process = None
    req = dict()

    if request.method == 'GET':
        process = request.args.get('process')
        req['param1'] = request.args.get('request')
        req['param2'] = request.args

    if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
        request_args = request.json.get('args')
        process = request_args.get('process')
        req['param1'] = request_args.get('request')
        req['param2'] = request_args

    if process == 'back_end':
        return back_end_handler(req=req)

    if process == 'front_end':
        return front_end_handler(req=req)

    return jsonify({'message': 'no route matched with those values'}), 200


@apis.errorhandler(404)
@apis.errorhandler(500)
def errorhandler(error):
    """errorhandler
    """
    return err_response(error=error), error.code
