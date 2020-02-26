from flask import render_template
from soundstream.routes import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/viz/<string:name>')
def render_viz(name):
    return render_template('viz_container.html', name=name)
