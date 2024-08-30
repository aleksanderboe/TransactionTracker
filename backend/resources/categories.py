from flask_restful import Resource, marshal_with, reqparse, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.category import Category
from ..db import db

import re

def name_length(value):
    if not (1 <= len(value) <= 20):
        raise ValueError("The length of the name must be between 1 and 20 characters")
    return value

def valid_color(value):
    if not re.match(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
        raise ValueError("Invalid color format. Provide a valid hex code.")
    return value

category_args = reqparse.RequestParser()
category_args.add_argument("name", type=name_length, required=True)
category_args.add_argument("color", type=valid_color, required=True)

category_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "color": fields.String
}

class CategoryResource(Resource):
    @jwt_required()
    @marshal_with(category_fields)
    def get(self, category_id):
        current_user_id = get_jwt_identity()
        category = Category.query.filter_by(id=category_id, user_id=current_user_id).first()
        if category:
            return category, 200
        else:
            return {"message": "Category not found"}, 404

    @jwt_required()
    def put(self, category_id):
        args = category_args.parse_args()
        current_user_id = get_jwt_identity()
        category = Category.query.filter_by(id=category_id, user_id=current_user_id).first()
        
        if category:
            category.name = args["name"]
            category.color = args["color"]
            db.session.commit()
            return {"message": "Category updated successfully"}, 200
        else:
            return {"message": "Category not found"}, 404

    @jwt_required()
    def delete(self, category_id):
        current_user_id = get_jwt_identity()
        category = Category.query.filter_by(id=category_id, user_id=current_user_id).first()
        
        if category:
            db.session.delete(category)
            db.session.commit()
            return {"message": "Category successfully deleted"}, 200
        else:
            return {"message": "Category not found"}, 404
        

class CategoryListResource(Resource):
    @jwt_required()
    @marshal_with(category_fields)
    def get(self):
        current_user_id = get_jwt_identity()
        categories = Category.query.filter_by(user_id=current_user_id).all()
        return categories, 200

    @jwt_required()
    def post(self):
        args = category_args.parse_args()
        current_user_id = get_jwt_identity()
        existing_category = Category.query.filter_by(name=args["name"], user_id=current_user_id).first()
        
        if existing_category:
            return {"message": "A category with this name already exists"}, 409 
        
        new_category = Category(name=args["name"], color=args["color"], user_id=current_user_id)
        db.session.add(new_category)
        db.session.commit()
        return {"message": "Category successfully added"}, 201