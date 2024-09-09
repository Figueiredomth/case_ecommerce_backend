from flask import Flask, jsonify, request
from models import db, User, Product, Order, init_db
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Define a secret key to secure the session
app.secret_key = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing the databse
init_db(app)

# Register Route 
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin', False) # Add the possibility to create admin users.

        hashed_password = generate_password_hash(password)

        # Data validation
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        if len(username) < 5 or len(password) < 8:
            return jsonify({"message": "Username must be at least 5 characters and password at least 8 characters"}), 400

        # Checking if the user already exists on database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        # Input the new user on database
        new_user = User(username=username, password=hashed_password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201

    # Other generic errors
    except Exception as e:   
        print(f"Error: {e}")
        return jsonify({"message": "Failed to register user"}), 400


if __name__ == '__main__':
    app.run(debug=True)