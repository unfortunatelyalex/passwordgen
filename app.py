import random
import logging
import traceback
from time import strftime
from waitress import serve
from werkzeug.exceptions import HTTPException
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request





app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-password', methods=['POST'])
def generate_password():
    length = int(request.form['length'])
    symbols = request.form.get('symbols', False)

    char_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    if symbols:
        char_set += '!?$%&*<>+-'

    password = ''
    for i in range(length):
        password += random.choice(char_set)

    password_groups = [password[i:i+5] for i in range(0, len(password), 5)]
    password_str = '-'.join(password_groups)
    return password_str
    
    

@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(HTTPException)
def exceptions(e):
    if isinstance(e, HTTPException):
        tb = traceback.format_exc()
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb)
        return e.status_code
    return render_template(e=e), 500



mode = 'prod'

if __name__ == '__main__':
    if mode == 'dev':
        app.run(host='127.0.0.1', port=8000, debug=True)
    elif mode == "prod":
        handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
        logger = logging.getLogger('tdm')
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)
        serve(app, host="127.0.0.1", port=8000)
