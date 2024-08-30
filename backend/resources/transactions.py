from flask_restful import Resource, reqparse, fields, marshal, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from datetime import datetime

from ..models.transaction import TransactionModel
from ..resources.categories import category_fields
from ..db import db

# Parsing incoming request data to ensure valid format and presence of required fields
transaction_args = reqparse.RequestParser()
transaction_args.add_argument("amount", type=float, required=True, help="Amount cannot be blank!")
transaction_args.add_argument("description", type=str, required=True, help="Description cannot be blank!")
transaction_args.add_argument("category_id", type=int, required=False, help="Category ID must be a valid integer if provided")
transaction_args.add_argument("type", type=str, required=True, help="Type must be expense or income", choices=("expense", "income"))
transaction_args.add_argument(
    "date",
    type=lambda x: datetime.strptime(x, '%Y-%m-%d'), 
    required=False,  
    default=datetime.now().strftime('%Y-%m-%d'), 
    help="Invalid date format, should be YYYY-MM-DD!"
)


# Fields for serializing the TransactionModel objects to JSON
class DateField(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')
    
transaction_fields = {
    "id": fields.Integer,
    "amount": fields.Float,
    "description": fields.String,
    "category": fields.Nested(category_fields, allow_null=True), 
    "type": fields.String,  
    "user_id": fields.Integer,
    "date_created": DateField()
}


class TransactionResource(Resource):
    @jwt_required()
    @marshal_with(transaction_fields)
    def get(self, transaction_id):
        current_user_id = get_jwt_identity()
        
        transaction = TransactionModel.query.filter_by(id=transaction_id, user_id=current_user_id).first()
        if transaction:
            return transaction, 200
        else:
            return {"message": "Transaction not found"}, 404

    @jwt_required()
    def put(self, transaction_id):
        args = transaction_args.parse_args()
        
        current_user_id = get_jwt_identity()

        transaction = TransactionModel.query.filter_by(id=transaction_id, user_id=current_user_id).first()

        if transaction:
            transaction.amount = args["amount"]
            transaction.description = args["description"]
            transaction.category_id = args.get("category_id") 
            transaction.type = args["type"]
            transaction.date_created = args["date"]

            db.session.commit()

            return {"message": "Transaction updated successfully"}, 200
        else:
            return {"message": "Transaction not found or unauthorized"}, 404

    @jwt_required()
    def delete(self, transaction_id):
        current_user_id = get_jwt_identity()
        
        transaction = TransactionModel.query.filter_by(id=transaction_id, user_id=current_user_id).first()
        
        if transaction:
            db.session.delete(transaction)
            db.session.commit()

            return {"message": "Transaction successfully deleted"}, 200
        else:
            return {"message": "Transaction failed to delete, not found"}, 404

class TransactionListResource(Resource):
    @jwt_required()
    def post(self):
        args = transaction_args.parse_args()
        
        current_user_id = get_jwt_identity()
        
        transaction = TransactionModel(amount=args["amount"],
                               description=args["description"],
                               category_id=args.get("category_id"), 
                               type=args["type"],
                               user_id=current_user_id,
                               date_created=args["date"])


        db.session.add(transaction)
        db.session.commit()

        return {"message": "Transaction successfully added"}, 201
    
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        
        transactions = TransactionModel.query.filter_by(user_id=current_user_id).all()
    
        if transactions:
            return marshal(transactions, transaction_fields, "data"), 202
        else:
            return {"data": [], "message": "You don't have any transactions added"}, 200
         

