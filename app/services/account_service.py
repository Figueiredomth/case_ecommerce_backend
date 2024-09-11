from flask import jsonify, session
from werkzeug.security import generate_password_hash
from app.models import User, db

def manage_account(user_id, data):
    if not user_id:
        return jsonify({"message": "No user is currently logged in"}), 401
    
    new_username = data.get('new_username', '').lower()
    new_password = data.get('new_password')

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
                session['username'] = new_username
            if new_password:
                user.password = generate_password_hash(new_password)
            db.session.commit()  # Commit the changes
            return jsonify({"message": "Account updated successfully!"})
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()  # Rollback if there's an error
        return jsonify({"message": "Failed to update account"}), 500

def get_account_info(user_id):
    if not user_id:
        return jsonify({"message": "No user is currently logged in"}), 401
    
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
