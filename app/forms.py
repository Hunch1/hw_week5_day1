from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class PokemonForm(FlaskForm):
    pokemon = StringField('pokemonNum:', validators=[DataRequired()])
    submit_btn = SubmitField('submit')

class LoginForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class SignupForm(FlaskForm):
    first_name = StringField('First Name: ', validators=[DataRequired()])
    last_name = StringField('Last Name ', validators=[DataRequired()])
    email = EmailField('Email ', validators=[DataRequired()])
    password = PasswordField('Password ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password ', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Register')