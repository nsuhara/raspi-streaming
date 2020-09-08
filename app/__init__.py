"""app/__init__.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
from flask import Flask

from app.config import config

app = Flask(__name__,
            static_folder='apis/static',
            template_folder='apis/templates')

app.config.from_object(config)

secret_key = app.secret_key
