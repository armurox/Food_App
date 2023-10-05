# Summary

This is a Flask web application for organizing and managing your kitchen ingredients and finding appropriate recipes based on those ingredients. The application allows users to perform OCR (Optical Character Recognition) on receipts to extract food items, manage their ingredients, and search for recipes.

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
   - Expiry dates of ingredients are obtained (as a heuristic at the moment), from the OpenAI API.

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

2. Install the required packages:

   ```
   pip3 install -r requirements.txt
   ```

3. Run the application:

   ```
   python app.py
   ```

   or 

   ```
   flask run
   ```


4. Access the application in your web browser at [http://localhost:5000/](http://localhost:5000/)., or click on the link that appears on the terminal after you run the program.

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

## Acknowledgments

This project was created with Flask, SQLite, the Spoonacular API and OpenAI API.