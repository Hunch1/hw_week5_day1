from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError


class PokemonForm(FlaskForm):
    pokemon = StringField('pokemonNum:', validators=[DataRequired()])
    submit_btn = SubmitField('submit')
    attacker_pokemon = SelectField('Select Attacker', coerce=int, validators=[DataRequired()])
    defender_pokemon = SelectField('Select Defender', coerce=int, validators=[DataRequired()])
    target_user = SelectField('Target User', choices=[], coerce=int)


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