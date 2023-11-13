from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import PokemonForm, LoginForm, SignupForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
# homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
# Pokemon stats
# import requests
# url = f'https://pokeapi.co/api/v2/pokemon/15'
# response = requests.get(url)
# print(type(response))
# response.status_code
# response.ok
# data = response.json()
@app.route('/Pokemon/stats', methods=['GET', 'POST'])
def get_pokemon_data():
    def get_pokemon_stats():
        # Accessing the 'stats' key from the JSON response
        stats = data['stats']
        pokemon_dict = {
            'Name': data['name'].title(),
            'Base Exp': data['base_experience'],
            'SpriteURL': data['sprites']['front_default']
        }
        for stat in stats:
            pokemon_dict[stat['stat']['name'].title()] = stat['base_stat']
        return pokemon_dict
    form = PokemonForm()
    # Made list to access multiple pokemon ids
    if request.method == 'POST':
        pokemon_id = form.pokemon.data
    # for pokemon_id in pokemon_ids:
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            pokemon_stats = get_pokemon_stats()
            return render_template('pokemonStats.html', stats=pokemon_stats.items(), form=form)
        else:
            return render_template('pokemomnStats.html', error_code = response.status_code, form=form)
    else:
        return render_template('pokemonStats.html', form=form)
    



REGISTERED_USERS = {}

    #  Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    


    # Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data 
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        # Create an instance of our User Class
        user = User(first_name, last_name, email, password)

        # add user to database
        db.session.add(user)
        db.session.commit()

        flash(f'Thank you for signing up {first_name}!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)
    


@app.route('/logout')
def logout():
        # Logout logic here
    return redirect(url_for('login'))