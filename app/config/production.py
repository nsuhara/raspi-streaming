"""app/config/production.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
import os

DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY', '')
JSON_AS_ASCII = False
