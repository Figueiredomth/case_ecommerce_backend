from flask import Flask, jsonify, request, session
from models import db, User, Product, Order, init_db
from werkzeug.security import generate_password_hash, check_password_hash

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
        username = data.get('username').lower() # convert to lower case
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

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Checking on database if the user already exists and if the password is correct 
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({"message": f"Welcome back, {user.username}!"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# Logout Route
@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        session.clear()
        return jsonify({"message": "Logged out successfully!"}), 200
    else:
        return jsonify({"message": "No user is currently logged in"}), 400

# Account management Route
@app.route('/account', methods=['GET', 'POST'])
def manage_account():
    user_id = session['user_id']
    
    if request.method == 'POST':
        data = request.get_json()
        new_username = data.get('new_username', '').lower()
        new_password = data.get('new_password')

        # Validate new_username and new_password
        if new_username:
            if len(new_username) < 5:
                return jsonify({"message": "Username must be at least 5 characters"}), 400
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({"message": "Username already taken"}), 400

        if new_password:
            if len(new_password) < 8:
                return jsonify({"message": "Password must be at least 8 characters"}), 400

        try:
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

    # Show account info
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

# Add product Route (only admin)
@app.route('/products', methods=['POST'])
def add_product():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401
    if not User.query.get(session['user_id']).is_admin:
        return jsonify({"message": "Admin access required"}), 403


    data = request.get_json()
    name = data.get('name').lower()  # Convert product name to lowercase to avoid case conflicts
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')

    # Missing values output
    if not name or price is None or stock is None:
        return jsonify({"message": "Name, price, and stock are required"}), 400

    # Check if product already exists
    existing_product = Product.query.filter_by(name=name).first()
    if existing_product:
        return jsonify({"message": "Product with this name already exists"}), 400
    
    # Validate price and stock are numeric
    try:
        price = float(price)
        stock = int(stock)
    except ValueError:
        return jsonify({"message": "Price and stock must be numeric values"}), 400

    # Validate price and stock are not negative
    if price < 0:
        return jsonify({"message": "Price cannot be negative"}), 400
    if stock < 0:
        return jsonify({"message": "Stock cannot be negative"}), 400

    try:
        new_product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to add product"}), 500


if __name__ == '__main__':
    app.run(debug=True)