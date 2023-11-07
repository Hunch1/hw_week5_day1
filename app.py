from flask import Flask, request, render_template
import requests
app = Flask(__name__)

# @app.route('/')
# @app.route('/home')
# def hello_thieves():
#     return '<h1>Hello Thieves, this is flask</h1>'


# Variable Rules
@app.route('/user/<username>')
def show_user(username):
    return f'Hello {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'This is post {post_id}'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'Successfully Logged in'
    else:
        return render_template('login.html')

# Showing backend data on the frontend
@app.route('/students')
def students():
    all_students = ['Maria', 'Alicia', 'Anthony']
    return render_template('students.html', all_students=all_students)



# homepage


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
    hold_pokemon_stats = []

    # Accessing the 'stats' key from the JSON response
    stats = data['stats']

    # Creating the dictionary for the Pokémon stats
    pokemon_dict = {
        'name': data['forms'][0]['name'],
        'base experience': data['base_experience'],
        'shiny sprite': data['sprites']['front_shiny'],
        'attack base stat': stats[1]['base_stat'],
        'hp base stat': stats[0]['base_stat'],
        'defense base stat': stats[2]['base_stat']
    }
    hold_pokemon_stats.append(pokemon_dict)

    return hold_pokemon_stats


#  made two diffrent functions to better understand accessing api
@app.route('/Pokemon/stats', methods=['GET', 'POST'])
def get_pokemon_data():
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
            return render_template('pokemonStats.html', pokemon_stats=pokemon_stats)
            all_pokemon_stats.append(pokemon_stats)
        except IndexError:
            print(f"Failed to fetch data for Pokemon with ID {pokemon_id}.")
    else:
        return render_template('pokemonStats.html')
    return all_pokemon_stats