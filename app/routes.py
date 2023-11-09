from flask import request, render_template
import requests
from app import app
from app.forms import PokemonForm, LoginForm, SignupForm
# homepage
@app.route('/')
@app.route('/home')
def home():
    return "Welcome! This is the home page."
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

        if email in REGISTERED_USERS and REGISTERED_USERS[email]['password'] == password:
            return f'Hello, {REGISTERED_USERS[email]["name"]}'
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    


    # Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        full_name = f'{form.first_name.data} {form.last_name.data}'
        email = form.email.data
        password = form.password.data
        
        REGISTERED_USERS[email] = {
            'name': full_name,
            'password': password
        }

        return f'Thank you for signing up {full_name}!'
    else:
        return render_template('signup.html', form=form)