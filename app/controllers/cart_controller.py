from flask import Blueprint, request, jsonify, session
from app.services.cart_service import CartService

cart_bp = Blueprint('cart', __name__)

# Add product to the cart route
@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    # Check for authentication
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    # Get the data of product and quantity in request
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)  # Default quantity to 1 if not provided

    # add product to the cart
    result = CartService.add_to_cart(session['user_id'], product_id, quantity)

    return result

# View cart route
@cart_bp.route('/view', methods=['GET'])
def view_cart():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    # view the cart
    result = CartService.view_cart(session['user_id'])

    return result

@cart_bp.route('/clear', methods=['DELETE'])
def clear_cart():
    # Check if the user is authenticated
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    # Call the service to clear the cart
    result = CartService.clear_cart(session['user_id'])

    return result