import random
from waitress import serve
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

mode = 'prod'

if __name__ == '__main__':
    if mode == 'dev':
        app.run(host='127.0.0.1', port=5000, debug=True)
    elif mode == "prod":
        serve(app, host="0.0.0.0", port=8000)
