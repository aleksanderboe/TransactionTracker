from flask import Blueprint, request, make_response, jsonify, send_from_directory, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask import current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import re

from ..models.user import UserModel
from ..db import db

auth = Blueprint("auth", __name__, url_prefix="/api/auth")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@auth.route('/upload-profile-picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    current_user_id = get_jwt_identity()
    user = UserModel.query.filter_by(id=current_user_id).first()
    
    if not user:
        return jsonify("User not found"), 404
    
    old_profile_picture = user.profile_picture

    if old_profile_picture:
        old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_profile_picture)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        user.profile_picture = filename
        db.session.commit()
        return jsonify(message="Profile picture uploaded successfully"), 200
    else:
        return jsonify(message="File not allowed. We only support PNG, GIF or JPG pictures"), 400
    
@auth.route('/uploads/<name>')
def download_file(name):
    filedir = current_app.config["UPLOAD_FOLDER"]
    safe_name = secure_filename(name)
    file_path = os.path.join(filedir, safe_name)

    if os.path.exists(file_path):
        return send_from_directory(filedir, safe_name)
    else:
        abort(404, description="File not found")

@auth.route("/user", methods=["GET"])
@jwt_required(optional=True)
def get_user():
    current_user_id = get_jwt_identity()
    
    if not current_user_id:
        return "User not found", 404

    user = UserModel.query.filter_by(id=current_user_id).first()
    if user:
        return jsonify(id=user.id, username=user.username, profile_picture=user.profile_picture)
    else:
        return "User not found", 404
    
@auth.route("/update-profile", methods=["PUT"])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    
    if not current_user_id:
        return jsonify({"message": "User not found"}), 404

    user = UserModel.query.filter_by(id=current_user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404
   
    data = request.json    
    username = data.get("username", "")
    password = data.get("password", "")
    
    if username: 
        username_error = validate_username(username)
        if username_error:
            return jsonify(message=username_error), 400
        
        user.username = username

    if password:
        password_error = validate_password(password)
        if password_error:
            return jsonify(message=password_error), 400
        
        user.password_hash = generate_password_hash(password)

    db.session.commit()
    
    return jsonify({"message": "Profile updated successfully"}), 200
   

@auth.route("/delete-account", methods=["POST"])
@jwt_required()
def delete_account():
    current_user_id = get_jwt_identity()
    
    if not current_user_id:
        return jsonify("User not found"), 404
    
    user = UserModel.query.filter_by(id=current_user_id).first()

    if not user:
        return jsonify("User not found"), 404
    
    if user.profile_picture:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user.profile_picture)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify("Account deleted"), 200


@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return jsonify(message="Username and password are required"), 400

    user = UserModel.query.filter_by(username=username).first() 

    if user and user.check_password(password):        
        access_token = create_access_token(identity=user.id)
        response = make_response(jsonify(access_token=access_token,  message="Login successful"), 200)
        return response        
    else:
        return jsonify(message="Invalid username or password"), 401


def validate_username(username):
    if not 3 <= len(username) <= 30:
        return 'Username needs to be between 3 and 30 characters'

    if UserModel.query.filter_by(username=username).first():
        return "Username already taken"

    return None

def validate_password(password):
    if not 8 <= len(password) <= 30:
        return 'Password needs to be between 8 and 30 characters'

    if not any(char.isupper() for char in password):
        return 'Password must contain at least one uppercase letter'

    if not any(char.islower() for char in password):
        return 'Password must contain at least one lowercase letter'

    if not any(char.isdigit() for char in password):
        return 'Password must contain at least one digit'

    if not re.search(r"[!@#$%^&*()\-_=+{}[\]|\\;:'\",.<>?/~`]", password):
        return 'Password must contain at least one special character'
    
    return None

@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return jsonify(message="Username and password are required"), 400

    username_error = validate_username(username)
    if username_error:
        return jsonify(message=username_error), 400

    password_error = validate_password(password)
    if password_error:
        return jsonify(message=password_error), 400
    
    password_hash = generate_password_hash(password)

    user = UserModel(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id)
    response = make_response(jsonify(access_token=access_token, message="Register successful"), 200)
    return response

@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():    
    return jsonify(message="Logout successful"), 200
