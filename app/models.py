from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

user_pokemon = db.Table(
    'user_pokemon',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    createdon = db.Column(db.DateTime, default=datetime.utcnow())
    pokemons = db.relationship('Pokemon', 
                           secondary=user_pokemon, 
                           back_populates='trainers',
                           lazy = 'dynamic'
                           )


    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    sprite_url = db.Column(db.String)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    trainers = db.relationship('User',
                              secondary=user_pokemon,
                              back_populates='pokemons',
                              lazy = 'dynamic'
                              )