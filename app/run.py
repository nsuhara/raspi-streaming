"""app/run.py
author          : nsuhara <na010210dv@gmail.com>
date created    : 2020/9/8
python version  : 3.7.3
"""
import os

from app import app
from app.apis.views.main_handler import apis
from app.common.utility import err_response

app.register_blueprint(apis)


@app.errorhandler(404)
@app.errorhandler(500)
def errorhandler(error):
    """errorhandler
    """
    return err_response(error=error), error.code


def main():
    """main
    """
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
