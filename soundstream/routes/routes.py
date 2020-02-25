from flask import render_template
from soundstream.routes import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/tunnel')
@main.route('/tunnel/<string:mode>')
def falling(mode='squares'):
    if mode not in ['squares', 'circles', 'bars']:
        mode = 'squares'
    return render_template('tunnel.html', mode=mode)
