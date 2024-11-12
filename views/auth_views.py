from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
from app import db

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity={'username': user.username, 'is_admin': user.is_admin})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401
