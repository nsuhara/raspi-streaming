"""app/apis/views/back_end_handler.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
from flask import Response, jsonify

from app import secret_key
from app.apis.views.camera import Camera


def handler(req):
    """handler
    """
    param1 = req.get('param1')
    param2 = req.get('param2')

    if param1 == 'video_feed':
        return _video_feed(req=param2)

    return jsonify({'message': 'no route matched with those values'}), 200


def _video_feed(req):
    """_video_feed
    """
    if req.get('secret_key', '') != secret_key:
        return jsonify({'message': 'no route matched with those values'}), 200
    return Response(_generator(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


def _generator(camera):
    """_generator
    """
    while True:
        frame = camera.frame()
        yield b'--frame\r\n'
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
