import logging

from flask import Flask
from flask import request

import kaput

import settings


app = Flask(__name__)
kaput.init(settings.API_KEY, settings.PROJECT_ID, debug=True)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/push', methods=['POST'])
def push():
    logging.error('request: %s' % request.data)
    return request.data, 200


if __name__ == '__main__':
    app.run()
