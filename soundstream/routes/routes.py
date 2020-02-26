from flask import render_template, current_app
from soundstream.routes import main
from soundstream.utils import get_list_of_visualizations


@main.route('/')
def index():
    viz_list = get_list_of_visualizations(current_app)
    return render_template('index.html', viz_list=viz_list)


@main.route('/viz/<string:name>')
def render_viz(name):
    return render_template('viz_container.html', name=name)
