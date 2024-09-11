from flask import Blueprint, request, jsonify, session
from app.services.product_service import add_product, edit_product, delete_product, list_products, details_products
from app.models import User

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/add', methods=['POST'])
def add_product_route():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401
    
    user = User.query.get(session['user_id'])
    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    if not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()
    return add_product(data)

@product_bp.route('/edit', methods=['PUT'])
def edit_product_route():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401
    
    user = User.query.get(session['user_id'])
    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    if not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()
    return edit_product(data)

@product_bp.route('/delete', methods=['DELETE'])
def delete_product_route():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401
    
    user = User.query.get(session['user_id'])
    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    if not user.is_admin:
        return jsonify({"message": "Admin access required"}), 403

    data = request.get_json()
    product_id = data.get('product_id')
    return delete_product(product_id)

@product_bp.route('/list', methods=['GET'])
def list_products_route():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    return list_products()

@product_bp.route('/details', methods=['GET'])
def details_products_route():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    return details_products()
