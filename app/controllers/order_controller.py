from flask import Blueprint, session, jsonify
from app.services.order_service import OrderService


order_bp = Blueprint('order', __name__)

# Make a order route
@order_bp.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    result, status = OrderService.place_order(session['user_id'])
    return jsonify(result), status