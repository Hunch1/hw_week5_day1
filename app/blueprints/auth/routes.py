from .import auth
from .forms import LoginForm, SignupForm, PokemonForm
from flask import request, flash, redirect, url_for, render_template
from app.models import User, db, Pokemon
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
import requests
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func



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
    

#
@auth.route('/logout')
def logout():
        # Logout logic here
    flash('Successfully logged out!', 'warning')
    logout_user()
    return redirect(url_for('auth.login'))


# og code
@auth.route('/Pokemon/stats', methods=['GET', 'POST'])
@login_required
def get_pokemon_data():
    def get_pokemon_stats(data):
        # Accessing the 'stats' key from the JSON response
        # kept just incase I break something
        stats = data['stats']
        pokemon_dict = {
            'ID': data['id'],
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
        pokemon_id = form.pokemon.data.strip()
        # Check if the entered ID is a digit (numeric value)
        if pokemon_id.isdigit():
            # If it's a digit, try to get the Pokémon from the database by ID
            pkmn = Pokemon.query.filter(Pokemon.id == int(pokemon_id)).first()
        else:
            # If it's not a digit, try to get the Pokémon from the database by name
            pkmn = Pokemon.query.filter(Pokemon.name == pokemon_id.title()).first()

        if pkmn:
            # If the Pokémon is in the database, display it
            pokemon_stats = get_pokemon_stats({
                'id': pkmn.id,
                'name': pkmn.name,
                'base_experience': pkmn.base_experience,
                'sprites': {'front_default': pkmn.sprite_url},
                'stats': [
                    {'base_stat': pkmn.hp, 'stat': {'name': 'hp'}},
                    {'base_stat': pkmn.attack, 'stat': {'name': 'attack'}},
                    {'base_stat': pkmn.defense, 'stat': {'name': 'defense'}},
                    {'base_stat': pkmn.speed, 'stat': {'name': 'speed'}}
                ]
            })
            return render_template('pokemonStats.html', stats=pokemon_stats.items(), form=form, pokemon_id=pokemon_id)
        else:
            # If the Pokémon is not in the database, fetch it from the PokeAPI
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
            response = requests.get(url)

            if response.ok:
                data = response.json()
                pokemon_stats = get_pokemon_stats(data)

                # Create a Pokemon instance and add it to the database
                new_pokemon = Pokemon(
                    id=data['id'],
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

                return render_template('pokemonStats.html', stats=pokemon_stats.items(), form=form, pokemon_id=pokemon_id)
            else:
                return render_template('pokemonStats.html', error_code=response.status_code, form=form)
    else:
        return render_template('pokemonStats.html', form=form)







@auth.route('/Pokemon/add_to_team/<string:pokemon_id>', methods=['POST'])
@login_required
def add_to_team(pokemon_id):
    # Ensure pokemon_id is not None and is a string
    selected_pokemon_id = str(pokemon_id).strip()

    if selected_pokemon_id.isdigit():
        # If it's a digit, try to get the Pokémon from the database by ID
        selected_pokemon = Pokemon.query.filter(Pokemon.id == int(selected_pokemon_id)).first()
    else:
        # If it's not a digit, try to get the Pokémon from the database by name (case-insensitive)
        selected_pokemon = Pokemon.query.filter(func.lower(Pokemon.name) == selected_pokemon_id.lower()).first()

    if selected_pokemon:
        # Check if the selected Pokemon is already in the user's team
        if selected_pokemon in current_user.pokemons:
            flash('You already have this Pokemon in your team.', 'warning')
        elif current_user.pokemons.count() >= 6:
            flash('Your team is already full. Remove a Pokemon before adding a new one.', 'danger')
        else:
            # Append the selected Pokemon to the user's team
            current_user.pokemons.append(selected_pokemon)
            db.session.commit()

            flash(f'{selected_pokemon.name} added to your team!', 'success')
    else:
        flash('Invalid Pokemon ID or name', 'danger')

    return redirect(url_for('auth.team'))






    
   







@auth.route('/team')
@login_required
def team():
    # Fetch the user's team from the database
    user_pokemons = current_user.pokemons.all()
    return render_template('team.html', user_pokemons=user_pokemons)



@auth.route('/Pokemon/clear_team', methods=['POST'])
@login_required
def clear_team():
    # Clear the user's team by removing all Pokemon
    current_user.pokemons = []
    db.session.commit()

    flash('Your team has been cleared!', 'success')
    return redirect(url_for('auth.team'))
