from flask import Blueprint, request, jsonify, session
from app.services.user_service import register_user, login_user, logout_user, manage_account

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

@user_bp.route('/logout', methods=['GET'])
def logout():
    return logout_user()

