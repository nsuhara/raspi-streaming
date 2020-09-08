"""app/common/utility.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
from flask import jsonify


def err_response(error):
    """err_response
    """
    return jsonify({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
