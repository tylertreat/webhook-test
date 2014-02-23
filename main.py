import logging

from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/push', methods=['POST'])
def push():
    logging.error('request: %s' % request.data)
    return request.data, 200


def foo():
    return 1 + 1


if __name__ == '__main__':
    app.run()
