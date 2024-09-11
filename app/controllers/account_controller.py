from flask import Blueprint, request, jsonify, session
from app.services.account_service import manage_account, get_account_info

account_bp = Blueprint('account_bp', __name__)

@account_bp.route('', methods=['GET', 'POST'])
def account():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401

    if request.method == 'POST':
        data = request.get_json()
        return manage_account(user_id, data)

    # GET method
    return get_account_info(user_id)
