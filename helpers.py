import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import openai
import pytesseract
from PIL import Image
import sqlite3

from flask import redirect, render_template, session
from functools import wraps

food_items_list = [
    "apple",
    "banana",
    "orange",
    "strawberries",
    "blueberries",
    "raspberries",
    "grapes",
    "watermelon",
    "pineapple",
    "mango",
    "kiwi",
    "avocado",
    "tomato",
    "cucumber",
    "carrot",
    "spinach",
    "lettuce",
    "broccoli",
    "cauliflower",
    "potato",
    "onion",
    "garlic",
    "chicken",
    "beef",
    "pork",
    "fish",
    "shrimp",
    "salmon",
    "tilapia",
    "eggs",
    "milk",
    "yogurt",
    "cheese",
    "butter",
    "bread",
    "rice",
    "pasta",
    "oats",
    "cereal",
    "flour",
    "sugar",
    "salt",
    "pepper",
    "olive oil",
    "vegetable oil",
    "ketchup",
    "mayonnaise",
    "mustard",
    "soy sauce",
    "vinegar",
    "honey",
    "peanut butter",
    "jam",
    "coffee",
    "tea",
    "chocolate",
    "cookies",
    "chips",
    "soda",
    "juice",
    "water",
    "ice cream",
    "frozen vegetables",
    "frozen pizza",
    "canned beans",
    "canned tomatoes",
    "canned soup",
    "snack bars",
    "granola",
    "nuts",
    "seeds",
    "red curry paste",    
]


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def perform_ocr(image_path):
    """Open image using imaging and read receipt using tesseract"""

    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def extract_food_items(text):
    """Parse text, store food items in DB for use in recipe."""

    text_lower = text.lower()
    # food_items = [item for item in food_items_list if item in text_lower]

    connection = sqlite3.connect("ingredients.db")
    cursor = connection.cursor()
    for item in food_items_list:
        if item in text_lower:
            cursor.execute("INSERT INTO ingredients (user_id, name) VALUES (?, ?)", (session["user_id"], item))
    connection.commit()
    # connection.close()


def remove_temp_image(image_path):
    import os
    os.remove(image_path)


def get_stored_ingredients():
    """Connect to and read DB, return ingredients for possible recipes."""

    connection = sqlite3.connect("ingredients.db")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM ingredients WHERE user_id = (?)", (session["user_id"],))
    ingredients = [row[0] for row in cursor.fetchall()]
    # connection.close()

    return ingredients

def get_recipes_for_ingredients(ingredients):
    """Connect to API, return recipes based on ingredients."""

    api_key = "50f9a9618ba54f559469cd1ca764904b"
    api_url = "https://api.spoonacular.com/recipes/findByIngredients"
    query_params = {
        "apiKey": api_key,
        "ingredients": ",".join(ingredients),
        "number": 5,  # Limiting to 5 recipes
        "ranking": 2 # minimize number of unused ingredients, trying only to use used ingredients
    }
    response = requests.get(api_url, params=query_params)
    recipes = response.json()
    return recipes


def ExpiryDate(ingredients):
    """Get expiry date for each ingredient in ingredients list."""
    openai.api_key = ""
    prompt = f"what is the expiry date of {ingredients}, Please answer with *Ingredient*: *ExpirationDate*, After each pair of values, seperate the next pair with a !" 
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )
    expiry = response.choices[0].text
    expiryList = expiry.strip().split("!")

    return expiryList
