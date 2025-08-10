from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
CSV_FILE = "recipes.csv"

def load_recipes():
    recipes = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name']
                brew_time = int(row['brew_time'])
                recipes.append((name, brew_time))
    return recipes

@app.route('/')
def index():
    recipes = load_recipes()
    return render_template('index.html', recipes=recipes)

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    name = request.form['name']
    brew_time = request.form['brew_time']

    # Append new recipe to CSV or create CSV if not exists
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['name', 'brew_time'])
        writer.writerow([name, brew_time])

    return redirect(url_for('index'))

@app.route('/start_timer/<int:brew_time>/<name>')
def start_timer(brew_time, name):
    return f"Starting timer for {name} - {brew_time} seconds"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
