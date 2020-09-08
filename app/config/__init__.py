"""app/config/__init__.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
import os

config = os.getenv('ENV_CONFIG', 'config.localhost')
