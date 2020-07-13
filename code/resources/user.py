from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help="The field 'username' is invalid.")
        self.parser.add_argument('password', type=str, required=True, help="The field 'password' is invalid.")
        self.parser.add_argument('first_name', type=str, required=True, help="The field 'first_name' is invalid.")
        self.parser.add_argument('last_name', type=str, required=True, help="The field 'last_name' is invalid.")
        self.parser.add_argument('is_admin', type=bool, required=False, help="The field 'is_admin' is invalid.")

    def post(self):
        data = self.parser.parse_args()

        if UserModel.query.filter_by(username=data['username']).first():
            return {'message': f"A user with the username '{data['username']}' is already registered."}, 400

        user = UserModel(**data)
        user.save()

        return {'message': 'User created successfully.'}, 201

class User(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help="The field 'username' is invalid.")
        self.parser.add_argument('first_name', type=str, required=True, help="The field 'first_name' is invalid.")
        self.parser.add_argument('last_name', type=str, required=True, help="The field 'last_name' is invalid.")
        self.parser.add_argument('is_admin', type=str, required=False, help="The field 'is_admin' is invalid.")
    
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()

        if user:
            return user.json()
        else:
            return {'message': 'Unable to find user.'}

    def post(self, id):
        user = UserModel.query.filter_by(id=id).first()

        if user is None:
            return {'message': 'Unable to find user.'}

        user.username = data['username']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.is_admin = datea['is_admin']
        user.save()

        return {'message': 'User successfully updated.'}

    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()

        if user is None:
            return {'message': 'Unable to find user'}

        user.delete()
        return {'message': 'User successfully deleted.'}

        

class UserList(Resource):

    def get(self):
        users = UserModel.query.all()
        return {'users': [user.json() for user in users]}

class UserPasswordReset(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('password', type=str, required=True, help="The field 'password' is invalid.")

    def post(self, id):
        data = self.parser.parse_args()

        user = UserModel.query.filter_by(id=id).first()
        user.password = data['password']

        if user is None:
            return {'message': 'Unable to find user.'}

        try:
            user.save()
        except:
            return {'message': 'There was an error resetting your password.'}

        return {'message': 'Password reset successful.'}