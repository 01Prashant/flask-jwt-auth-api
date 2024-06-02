# Flask API with JWT Authentication and Token Revocation

This project is a Flask API that supports user authentication using JWT (JSON Web Tokens). It includes features such as user signup, login, profile management, and token revocation (logout).

## Features

- User Signup
- User Login
- Retrieve User Profile
- Update User Profile
- Delete User Profile
- Token Revocation (Logout)

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/01Prashant/flask-jwt-auth-api
   cd flask-jwt-auth-api


2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt

4. **Set up the database:**
   1. Configure your database settings in config.py.
   2. Initialize the database:
   ```sh
   flask db upgrade

## Configuration

Edit the config.py file to set up your database and secret key for JWT. Example configuration:

