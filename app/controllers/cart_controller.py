from flask import Blueprint, request, jsonify, session
from app.services.cart_service import CartService

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    # Verifica se o usuário está autenticado
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    # Obtém os dados do produto e quantidade da requisição
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)  # Default quantity to 1 if not provided

    # Chama o serviço para adicionar o produto ao carrinho
    result = CartService.add_to_cart(session['user_id'], product_id, quantity)

    return result

@cart_bp.route('/view', methods=['GET'])
def view_cart():
    # Verifica se o usuário está autenticado
    if 'user_id' not in session:
        return jsonify({"message": "Authentication required"}), 401

    # Chama o serviço para visualizar o carrinho
    result = CartService.view_cart(session['user_id'])

    return result
