from __future__ import (absolute_import, division, print_function)

import spyne
import logging

import wof
import wof.flask
from test_dao import TestDao

logging.basicConfig(level=logging.DEBUG)


def create_app():
    test_dao = TestDao()
    app = wof.flask.create_wof_flask_app(test_dao, 'test_config.cfg')
    app.config['DEBUG'] = True

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, threaded=True)
