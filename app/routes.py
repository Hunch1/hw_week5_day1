from flask import request, render_template
import requests
from app import app
from app.forms import PokemonForm



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

def get_pokemon_stats(data):
    form = PokemonForm()
    hold_pokemon_stats = []

    # Accessing the 'stats' key from the JSON response
    stats = data['stats']

    # Creating the dictionary for the Pokémon stats
    pokemon_dict = {
        'name': data.get['forms'][0]['name'],
        'base experience': data['base_experience'],
        'shiny sprite': data['sprites']['front_shiny'],
        'attack base stat': stats[1]['base_stat'],
        'hp base stat': stats[0]['base_stat'],
        'defense base stat': stats[2]['base_stat']
    }
    hold_pokemon_stats.append(pokemon_dict)
    return hold_pokemon_stats


@app.route('/Pokemon/stats', methods=['GET', 'POST'])
def get_pokemon_data():
    form = PokemonForm()
    all_pokemon_stats = []
    # Made list to access multiple pokemon ids
    if request.method == 'POST':
        pokemon_id = request.form.get('pokemon_id')
    # for pokemon_id in pokemon_ids:
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
        try:
            response = requests.get(url)
            new_data = response.json()
            pokemon_stats = get_pokemon_stats(new_data)
            return render_template('pokemonStats.html', stats=all_pokemon_stats) 
            all_pokemon_stats.append(pokemon_stats)
        except IndexError:
            print(f"Failed to fetch data for Pokemon with ID {pokemon_id}.")
    else:
        return render_template('pokemonStats.html', form=form)
    return all_pokemon_stats