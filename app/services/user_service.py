from flask import jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db

# Function to register a new user
def register_user(data):
    try:
        username = data.get('username', '').lower()  # Convert to lowercase to ensure case-insensitivity
        password = data.get('password')
        is_admin = data.get('is_admin', False)  # Admin flag, default to False

        # Validate data
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        if len(username) < 5 or len(password) < 8:
            return jsonify({"message": "Username must be at least 5 characters and password at least 8 characters"}), 400

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({"message": "User already exists"}), 400

        # Create new user with hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to register user"}), 400

# Function to log in a user
def login_user(data):
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({"message": f"Welcome back, {user.username}!"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# Function to log out the current user
def logout_user():
    if 'user_id' in session:
        session.clear()
        return jsonify({"message": "Logged out successfully!"}), 200
    else:
        return jsonify({"message": "No user is currently logged in"}), 400

# Function to manage account details
def manage_account(user_id, data):
    try:
        new_username = data.get('new_username', '').lower()
        new_password = data.get('new_password')

        if new_username:
            if len(new_username) < 5:
                return jsonify({"message": "Username must be at least 5 characters"}), 400
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({"message": "Username already taken"}), 400

        if new_password:
            if len(new_password) < 8:
                return jsonify({"message": "Password must be at least 8 characters"}), 400

        user = User.query.get(user_id)
        if user:
            if new_username:
                user.username = new_username
                session['username'] = new_username  # Update username in session
            if new_password:
                user.password = generate_password_hash(new_password)
            db.session.commit()
            return jsonify({"message": "Account updated successfully!"})
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to update account"}), 500

# Function to get account information
def get_account_info(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                "user_id": user.id,
                "username": user.username
            }), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to retrieve account information"}), 500
