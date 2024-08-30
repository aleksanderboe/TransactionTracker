from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from datetime import timedelta
import os

from . import  models, routes
from .resources.transactions import TransactionResource, TransactionListResource
from .resources.categories import CategoryResource, CategoryListResource

def create_app():
    dir = os.path.abspath(os.path.dirname(__file__))

    instace_path = os.path.join(dir, "instance")

    UPLOAD_FOLDER =  os.path.join(dir, "images")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app = Flask(__name__, instance_path=instace_path)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['SECRET_KEY'] = "insert_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development') 

    jwt = JWTManager(app)

    CORS(app, supports_credentials=True)

    api = Api(app)
    api.add_resource(TransactionResource, "/api/transactions/<transaction_id>")
    api.add_resource(TransactionListResource, "/api/transactions")
    api.add_resource(CategoryResource, '/api/categories/<int:category_id>')
    api.add_resource(CategoryListResource, '/api/categories')

    models.init_app(app)
    routes.init_app(app)
    
    if app.config["ENV"] == "production":
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve(path):
            static_folder = os.path.join(dir, '../frontend/dist')
            if path != "" and os.path.exists(os.path.join(static_folder, path)):
                return send_from_directory(static_folder, path)
            else:
                return send_from_directory(static_folder, 'index.html')
        
    return app