from flask import Flask, request, make_response, render_template, session, redirect, flash
from flask_session import Session
import requests
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, perform_ocr, extract_food_items, remove_temp_image, get_stored_ingredients, get_recipes_for_ingredients, ExpiryDate

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Create a SQLite database, enabling multithreading
connection = sqlite3.connect("ingredients.db", check_same_thread=False)
# Enable conversion of data to a list of dictionaries
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
"""Set up database for the first time"""
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, hash TEXT NOT NULL)")

# To speed up username and user_id searches and ensure that usernames are unique
cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username)")

cursor.execute("CREATE TABLE IF NOT EXISTS ingredients (user_id INTEGER NOT NULL, name TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")

# Similarly to speed up ingredient searches and ensure that ingredient names are unique
cursor.execute("CREATE INDEX IF NOT EXISTS name ON ingredients (name)")

# Speed up lookup of all ingredients associated with a particular user
cursor.execute("CREATE INDEX IF NOT EXISTS user_id ON ingredients (user_id)")
connection.commit()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Main part of the program, providing recipes"""
    connection = sqlite3.connect("ingredients.db", check_same_thread=False)
    # Enable conversion of data to a list of dictionaries
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    # Enable the uploading of a new receipt
    if request.method == "GET":
        cursor.execute("DELETE FROM ingredients WHERE user_id = (?)", (session["user_id"],))
        connection.commit()
        return render_template("index.html")
    
    elif request.method == "POST":
        connection.close()
        image = request.files["image"]

        temp_path = "temp_image.jpg"
        image.save(temp_path)

        extracted_text = perform_ocr(temp_path)

        remove_temp_image(temp_path)

        # food_items
        
        extract_food_items(extracted_text)

        stored_ingredients = get_stored_ingredients()

        recipes = get_recipes_for_ingredients(stored_ingredients)
        
        dates = ExpiryDate(stored_ingredients)
         
        return render_template("data.html", dates = dates, extracted_text = extracted_text, recipes = recipes)

@app.route("/instructions", methods = ["POST"])
@login_required
def instructions():
    """Get detailed instructions for recipes"""
    id = request.form.get("id")
    item = []
    item.append(request.form.get("name"))
    item.append(request.form.get("image"))
    item.append(request.form.get("items").replace("[", "").replace("]", "").split("'"))
    api_url = f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions"
    api_key = "50f9a9618ba54f559469cd1ca764904b"
    query_params = {
        "apiKey": api_key,
        "stepBreakdown": "true"
    }
    # Get step-by-step instruction
    response = requests.get(api_url, params=query_params)
    instructions = response.json()
    # Get recipe summary
    api_url = f"https://api.spoonacular.com/recipes/{id}/summary"
    query_params = {
        "apiKey": api_key
    }
    response = requests.get(api_url, params=query_params)
    info = response.json()
    return render_template("instructions.html", item = item, instructions = instructions, info = info) 
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Please provide a username", 400)
        database_username = cursor.execute("SELECT username FROM users WHERE username = (?)", (username,))
        database_username = [dict(i) for i in database_username]
        if  len(database_username) > 0:
            return apology("username already exists", 400)
        password = request.form.get("password")
        password_check = request.form.get("confirmation")
        if password != password_check or not password:
            return apology("passwords do not match / did not enter a password", 400)
        # Register user
        cursor.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, generate_password_hash(password)))
        connection.commit()
        user = cursor.execute("SELECT id FROM users WHERE username = (?)", (username,))
        user = [dict(i) for i in user]
        # Log user in  after registration
        session["user_id"] = user[0]["id"]
        flash("Registered!")
        return redirect("/")
    
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = cursor.execute("SELECT * FROM users WHERE username = (?)", (request.form.get("username"),))

        rows = [dict(i) for i in rows]
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/password-change", methods=["GET", "POST"])
@login_required
def password_change():
    """Enable password changes"""
    if request.method == "GET":
        return render_template("password_change.html")
    prev_password = cursor.execute("SELECT * FROM users WHERE id = (?)", (session["user_id"],))
    prev_password = [dict(i) for i in prev_password]
    prev_password = prev_password[0]["hash"]
    if not check_password_hash(prev_password, request.form.get("curr_password")):
        return apology("Invalid Current Password", 400)
    new_password = request.form.get("new_password")
    if new_password != request.form.get("confirmation") or not new_password:
        return apology(
            "Please make sure you have confirmed your password / chosen a new password",
            400,
        )
    cursor.execute(
        "UPDATE users SET hash = (?) WHERE id = (?)",
        (generate_password_hash(new_password),
        session["user_id"])
    )
    connection.commit()
    flash("Password Changed!")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)
