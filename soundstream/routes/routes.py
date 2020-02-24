from flask import render_template
from soundstream.routes import main


@main.route('/')
def index():
    return render_template('index.html')
