from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from models import db, User, RevokedToken
from config import Config
import uuid
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma = Marshmallow(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Define User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Generate JWT token
def generate_token(user_id):
    jti = str(uuid.uuid4())
    payload = {
        'user_id': user_id,
        'jti': jti,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=1)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token, jti

# Verify JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Token validation decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'message': 'Error decoding token', 'error': str(e)}), 401

        if is_token_revoked(payload['jti']):
            return jsonify({'message': 'Token has been revoked'}), 401

        # Add user_id to kwargs for use in the protected endpoint
        kwargs['user_id'] = user_id
        return f(*args, **kwargs)

    return decorated

# Token blacklisting functions
def is_token_revoked(jti):
    """Check if the token is revoked"""
    return bool(RevokedToken.query.filter_by(jti=jti).first())

def revoke_token(jti):
    """Revoke a token by adding it to the blacklist"""
    if not is_token_revoked(jti):
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()

# SignUp API
@app.route('/signup/', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

# Login API
@app.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token, jti = generate_token(user.id)  # Update to include jti
    return jsonify({'token': token}), 200

# Retrieve User Profile API
@app.route('/profile/<int:user_id>/', methods=['GET'])
@token_required
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        return user_schema.jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

# Update User Profile API
@app.route('/profile/<int:user_id>/', methods=['PUT'])
@token_required
def update_user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.other_profile_data = data.get('other_profile_data', user.other_profile_data)
        db.session.commit()
        return user_schema.jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

# Delete User Profile API
@app.route('/profile/<int:user_id>/', methods=['DELETE'])
@token_required
def delete_user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User profile deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

# Logout API
@app.route('/logout/', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]  # Extract token from header
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            jti = decoded_token['jti']  # Extract JWT ID
            revoke_token(jti)  # Revoke the token
            return jsonify({'message': 'Logout successful'}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
    else:
        return jsonify({'error': 'Authorization header is missing'}), 401

# Main
if __name__ == '__main__':
    app.run(debug=True)
