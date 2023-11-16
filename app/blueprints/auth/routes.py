from .import auth
from .forms import LoginForm, SignupForm, PokemonForm
from flask import request, flash, redirect, url_for, render_template
from app.models import User, db, Pokemon
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import requests




REGISTERED_USERS = {}

    #  Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, {queried_user.first_name}!', 'success')
            return redirect(url_for('main.home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    


    # Signup
@auth.route('/signup', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=form)
    


@auth.route('/logout')
def logout():
        # Logout logic here
    flash('Successfully logged out!', 'warning')
    logout_user()
    return redirect(url_for('auth.login'))


# Pokemon stats
# import requests
# url = f'https://pokeapi.co/api/v2/pokemon/15'
# response = requests.get(url)
# print(type(response))
# response.status_code
# response.ok
# data = response.json()
@auth.route('/Pokemon/stats', methods=['GET', 'POST'])
@login_required
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

              # Create a Pokemon instance and add it to the database
            new_pokemon = Pokemon(
                name=data['name'].title(),
                base_experience=data['base_experience'],
                sprite_url=data['sprites']['front_default'],
                hp=data['stats'][0]['base_stat'],
                attack=data['stats'][1]['base_stat'],
                defense=data['stats'][2]['base_stat'],
                speed=data['stats'][5]['base_stat'],

            )

            db.session.add(new_pokemon)
            db.session.commit()

            return render_template('pokemonStats.html', stats=pokemon_stats.items(), form=form)
        else:
            return render_template('pokemonStats.html', error_code = response.status_code, form=form)
    else:
        return render_template('pokemonStats.html', form=form)
    
   

   
@auth.route('/Pokemon/add_to_team', methods=['POST'])
@login_required
def add_to_team():
    form = PokemonForm()

    if request.method == 'POST' and form.validate_on_submit():
        pokemon_id = form.pokemon.data

        # Check if the selected Pokemon is already in the user's team
        if Pokemon.query.filter(Pokemon.id == pokemon_id, Pokemon.trainers.contains(current_user)).first():
            flash('You already have this Pokemon in your team.', 'warning')
        elif len(current_user.pokemons) >= 6:
            flash('Your team is already full. Remove a Pokemon before adding a new one.', 'danger')
        else:
            # Fetch the selected Pokemon from the database
            selected_pokemon = Pokemon.query.get(pokemon_id)

            if selected_pokemon:
                # Append the selected Pokemon to the user's team
                current_user.pokemons.append(selected_pokemon)
                db.session.commit()

                flash('Pokemon added to your team!', 'success')
            else:
                flash('Invalid Pokemon ID', 'danger')

    return redirect(url_for('auth.get_pokemon_data'))