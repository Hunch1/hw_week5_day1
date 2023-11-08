from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonForm(FlaskForm):
    pokemon = StringField('pokemonNum:', validators=[DataRequired()])
    submit_btn = SubmitField('submit')