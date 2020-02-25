from flask import render_template
from soundstream.routes import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/viz/spectro')
def spectro():
    return render_template('viz/spectro.html')


@main.route('/viz/tunnel')
@main.route('/viz/tunnel/<string:mode>')
def falling(mode='squares'):
    if mode not in ['squares', 'circles', 'bars']:
        mode = 'squares'
    return render_template('viz/tunnel.html', mode=mode)
