from flask import render_template
from soundstream.routes import main
from soundstream.viz_index import viz_index


@main.route('/')
def index():
    return render_template('index.html', viz_index=viz_index)


@main.route('/viz/<string:name>')
def render_viz(name):
    return render_template('viz_container.html', name=name)
