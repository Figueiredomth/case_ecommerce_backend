from flask import jsonify
from app.models import Product, db

def add_product(data):
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
        db.session.rollback()
        return jsonify({"message": "Failed to add product"}), 500

def edit_product(data):
    product_id = data.get('product_id')
    name = data.get('name').lower() if data.get('name') else None  # Convert name to lowercase to avoid case conflicts
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')

    if not product_id:
        return jsonify({"message": "Product ID is required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    if not name and price is None and stock is None:
        return jsonify({"message": "At least one field (name, price, or stock) must be provided for update"}), 400

    if name:
        existing_product = Product.query.filter_by(name=name).first()
        if existing_product and existing_product.id != product_id:
            return jsonify({"message": "Product with this name already exists"}), 400

    try:
        if price is not None:
            price = float(price)
        if stock is not None:
            stock = int(stock)
    except ValueError:
        return jsonify({"message": "Price and stock must be numeric values"}), 400

    if price is not None and price < 0:
        return jsonify({"message": "Price cannot be negative"}), 400
    if stock is not None and stock < 0:
        return jsonify({"message": "Stock cannot be negative"}), 400

    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock

    try:
        db.session.commit()
        return jsonify({"message": "Product updated successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({"message": "Failed to update product"}), 500

def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return jsonify({"message": "Failed to delete product"}), 500

def list_products():
    try:
        products = Product.query.all()
        if not products:
            return jsonify({"message": "No products available"}), 404

        product_list = [{"name": p.name, "stock": p.stock} for p in products]
        return jsonify(product_list), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to retrieve products"}), 500

def details_products():
    try:
        products = Product.query.all()
        if not products:
            return jsonify({"message": "No products available"}), 404

        product_list = [{"name": p.name, "description": p.description, "price": p.price} for p in products]
        return jsonify(product_list), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to retrieve products"}), 500
