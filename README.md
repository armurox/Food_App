# How to use the current website changes made to the repo
1. Clone this repo
2. Install all dependencies (including recently added ones) with `pip3 install -r requirements.txt` or `pip install -r requirements.txt` for python versions before 3.x
3. If everything's present either python3 app.py or flask run should work, and click on the link (which should be 127.0.0.1)

# Recipe Organizer README

This is a Flask web application for organizing and managing your kitchen ingredients and finding recipes based on those ingredients. The application allows users to perform OCR (Optical Character Recognition) on receipts to extract food items, manage their ingredients, and search for recipes.

## Features

1. **User Registration and Login**
   - Users can register for an account with a unique username and a secure password.
   - Existing users can log in to their accounts.
   - Passwords are securely hashed and stored in the database.

2. **Password Change**
   - Logged-in users can change their passwords securely.

3. **Ingredient Management**
   - Users can upload a receipt image.
   - The application performs OCR on the receipt to extract food items.
   - Users can view the extracted food items and their expiry dates.
   - Ingredients are associated with the user's account for future reference.

4. **Recipe Search**
   - Users can search for recipes based on the ingredients they have stored.
   - The application retrieves recipes using the Spoonacular API, providing detailed instructions and information about the recipes.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Flask
- Flask-Session
- Requests
- SQLite3
- Werkzeug

## Getting Started

1. Clone the repository to your local machine.

2. Set up a virtual environment and install the required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   pip install -r requirements.txt
   ```

3. Create a new SQLite database named `ingredients.db`:

   ```bash
   touch ingredients.db
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Access the application in your web browser at [http://localhost:5000/](http://localhost:5000/).

## Usage

1. **Registration and Login**
   - Register for an account or log in with your existing credentials.

2. **Uploading a Receipt**
   - On the homepage, you can upload a receipt image.
   - The application will extract food items from the receipt using OCR.

3. **Managing Ingredients**
   - View the extracted food items and their expiry dates on the homepage.
   - Ingredients are associated with your account.

4. **Searching for Recipes**
   - Click on an ingredient to view recipes that use that ingredient.
   - The application retrieves recipes from the Spoonacular API and displays step-by-step instructions and recipe information.

5. **Changing Password**
   - If you are logged in, you can change your password by navigating to the "Change Password" page.

6. **Logging Out**
   - To log out of your account, click the "Logout" button.

## Contributing

If you want to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.

## Acknowledgments

This project was created with Flask, SQLite, and the Spoonacular API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.