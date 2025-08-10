from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

DB_FILE = "database.db"
CSV_FILE = "recipes.csv"

# Create DB if it doesn't exist
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brew_time INTEGER NOT NULL
            )
        """)
    # If recipes.csv exists, load it into DB
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        with sqlite3.connect(DB_FILE) as conn:
            df.to_sql("recipes", conn, if_exists="replace", index=False)

init_db()

@app.route("/")
def index():
    with sqlite3.connect(DB_FILE) as conn:
        recipes = conn.execute("SELECT * FROM recipes").fetchall()
    return render_template("index.html", recipes=recipes)

@app.route("/start_timer/<int:brew_time>/<name>")
def start_timer(brew_time, name):
    return render_template("timer.html", brew_time=brew_time, coffee_name=name)

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    name = request.form["name"]
    brew_time = int(request.form["brew_time"])
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO recipes (name, brew_time) VALUES (?, ?)", (name, brew_time))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
