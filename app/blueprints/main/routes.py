from app.blueprints.main import main
from flask import render_template, request
from flask_login import login_required
import requests
from app.models import db, Pokemon

@main.route('/')
@main.route('/home')
def home():
    # x = Pokemon.query.all()
    # for p in x:
    #     db.session.delete(p)
    # db.session.commit()

    return render_template('home.html')

