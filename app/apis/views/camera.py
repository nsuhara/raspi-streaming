"""app/apis/views/camera.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
import cv2


class Camera():
    """Camera
    """

    def __init__(self):
        self.video_capture = cv2.VideoCapture(-1)

    def __del__(self):
        self.video_capture.release()

    def frame(self):
        """frame
        """
        _, frame = self.video_capture.read()
        _, image = cv2.imencode('.jpeg', frame)
        return image.tobytes()
