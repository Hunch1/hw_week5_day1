from app.blueprints.main import main
from flask import render_template, request
from flask_login import login_required
import requests

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')