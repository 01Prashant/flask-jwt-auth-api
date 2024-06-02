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

1. Edit the config.py file to set up your database and secret key for JWT. Example configuration:

   ```sh
   class Config:
      SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
      SQLALCHEMY_TRACK_MODIFICATIONS = False
      SECRET_KEY = 'your_secret_key'
## Running the Application

1. **Run the Flask application:**

   ```shflask run
   flask run
2. The API will be accessible at http://127.0.0.1:5000/.

## API Endpoints

**User Registration**

1. Endpoint: '/signup/'
2. Method: POST
3. Payload:

   ```shflask run
   {
    "name": "Prashant Srivastava",
    "email": "prashant@example.com",
    "password": "password123"
   }
**User Login**

1. Endpoint: '/login/'
2. Method: POST
3. Payload:

   ```shflask run
   {
    "email": "prashant@example.com",
    "password": "password123"
   }
4. Response:

   ```shflask run
   {
    "token": "your_jwt_token"
   }
**Retrieve User Profile**

1. Endpoint: '/profile/<int:user_id>/'
2. Method: GET
3. Headers:

   ```shflask run
   Authorization: Bearer your_jwt_token
**Update User Profile**

1. Endpoint: '/profile/<int:user_id>/'
2. Method: PUT
3. Headers:

   ```shflask run
   Authorization: Bearer your_jwt_token
4. Payload:

   ```shflask run
   {
    "name": "Prashant Srivastava Updated",
    "other_profile_data": "Other data"
   }
**Delete User Profile**

1. Endpoint: '/profile/<int:user_id>/'
2. Method: DELETE
3. Headers:

   ```shflask run
   Authorization: Bearer your_jwt_token
**Logout**

1. Endpoint: '/logout/'
2. Method: POST
3. Headers:

   ```shflask run
   Authorization: Bearer your_jwt_token
## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
