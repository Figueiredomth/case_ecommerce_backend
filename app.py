from flask import Flask, jsonify, request, session
from models import db, User, Product, Order, OrderItem, Cart, init_db
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
@app.route('/products/add', methods=['POST'])
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


# Edit product Route (only admin)
@app.route('/products/edit', methods=['PUT'])
def edit_product():
    # Check if the user is logged in and is an admin
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401
    if not User.query.get(session['user_id']).is_admin:
        return jsonify({"message": "Admin access required"}), 403

    # Get data from the request
    data = request.get_json()
    product_id = data.get('product_id')
    name = data.get('name').lower() if data.get('name') else None  # Convert name to lowercase to avoid case conflicts
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')

    # Validate that product_id is provided
    if not product_id:
        return jsonify({"message": "Product ID is required"}), 400

    # Fetch the product from the database
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # Check if name, price, and stock are missing (as required fields)
    if not name and price is None and stock is None:
        return jsonify({"message": "At least one field (name, price, or stock) must be provided for update"}), 400

    # Check if a product with the same name already exists (case insensitive)
    if name:
        existing_product = Product.query.filter_by(name=name).first()
        if existing_product and existing_product.id != product_id:
            return jsonify({"message": "Product with this name already exists"}), 400

    # Validate price and stock if provided
    try:
        if price is not None:
            price = float(price)
        if stock is not None:
            stock = int(stock)
    except ValueError:
        return jsonify({"message": "Price and stock must be numeric values"}), 400

    # Validate price and stock are not negative
    if price is not None and price      < 0:
        return jsonify({"message": "Price cannot be negative"}), 400
    if stock is not None and stock < 0:
        return jsonify({"message": "Stock cannot be negative"}), 400

    # Update product details if provided
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock

    # Commit changes to the database
    try:
        db.session.commit()
        return jsonify({"message": "Product updated successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to update product"}), 500

# Delete product Route (only admin)
@app.route('/products/delete', methods=['DELETE'])
def delete_product():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401
    if not User.query.get(session['user_id']).is_admin:
        return jsonify({"message": "Admin access required"}), 403

    # Get product_id from the request and validate
    data = request.get_json()
    product_id = data.get('product_id')
    if not product_id:
        return jsonify({"message": "Product ID is required"}), 400

    # Fetch the product from the database
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # Delete the product
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to delete product"}), 500

# List products Route
@app.route('/products/list', methods=['GET'])
def list_products():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    try:
        # Fetch all products from the database
        products = Product.query.all()
        if not products:
            return jsonify({"message": "No products available"}), 404

        # Create a list of products with relevant details
        product_list = [{"name": p.name, "stock": p.stock} for p in products]

        return jsonify(product_list), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to retrieve products"}), 500


# List details of products Route
@app.route('/products/details', methods=['GET'])
def details_products():
    # Check if the user is logged in
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    try:
        # Fetch all products from the database
        products = Product.query.all()
        if not products:
            return jsonify({"message": "No products available"}), 404

        # Create a list of products with relevant details
        product_list = [{"name": p.name, "description": p.description, "price": p.price} for p in products]
        
        return jsonify(product_list), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to retrieve products"}), 500
    

# add product on cart Route
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    # Validate that product_id and quantity are provided
    if not product_id or quantity <= 0:
        return jsonify({"message": "Product ID and valid quantity are required"}), 400

    # Fetch the product from the database
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    # Check if there's enough stock
    if product.stock < quantity:
        return jsonify({"message": "Not enough stock available"}), 400

    # Add the product to the cart (cart could be a separate table or stored in session)
    try:
        cart_item = Cart(user_id=session['user_id'], product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({"message": "Product added to cart successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to add product to cart"}), 500
    
# View cart Route
@app.route('/cart/view', methods=['GET'])
def view_cart():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    try:
        # Fetch cart items for the user
        cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
        if not cart_items:
            return jsonify({"message": "Cart is empty"}), 404

        # Create a list of cart items with relevant details
        cart_list = [{
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price_per_item": item.product.price,
            "total_price": item.quantity * item.product.price
        } for item in cart_items]

        return jsonify(cart_list), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to retrieve cart items"}), 500

# Order route
@app.route('/cart/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    try:
        # Fetch cart items for the user
        cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
        if not cart_items:
            return jsonify({"message": "Cart is empty"}), 404

        total_price = sum(item.quantity * item.product.price for item in cart_items)

        # Create a new order
        order = Order(user_id=session['user_id'], total=total_price)
        db.session.add(order)
        db.session.commit()

        # Create order items based on cart
        for item in cart_items:
            # Fetch the product to ensure we have the correct price
            product = Product.query.get(item.product_id)
            if product is None:
                return jsonify({"message": f"Product with ID {item.product_id} not found"}), 404

            order_item = OrderItem(
                order_id=order.id, 
                product_id=item.product_id, 
                quantity=item.quantity,
                price=product.price  # Use the price from the product
            )
            db.session.add(order_item)

            # Decrease stock of the product
            product.stock -= item.quantity
            db.session.add(product)  # Ensure the product update is added to the session

        # Clear the cart
        Cart.query.filter_by(user_id=session['user_id']).delete()
        db.session.commit()

        return jsonify({"message": "Order placed successfully!", "order_id": order.id}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to place order"}), 500


if __name__ == '__main__':
    app.run(debug=True)