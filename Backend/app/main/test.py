from flask import render_template
from . import main

@main.route('/')
def test_page():
    return render_template('test.html')