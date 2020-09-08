"""app/apis/views/front_end_handler.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
from flask import jsonify, render_template

from app import secret_key


def handler(req):
    """handler
    """
    param1 = req.get('param1')
    param2 = req.get('param2')

    if param1 == 'app_form':
        return _app_form(req=param2)

    return jsonify({'message': 'no route matched with those values'}), 200


def _app_form(req):
    """_app_form
    """
    if req.get('secret_key', '') != secret_key:
        return jsonify({'message': 'no route matched with those values'}), 200
    return render_template('app_form.html', secret_key=req.get('secret_key', ''))
