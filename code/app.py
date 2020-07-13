from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import User, UserList, UserPasswordReset, UserRegister
from resources.shift import Shift, ShiftList, ShiftClockIn, ShiftClockOut

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dynamic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'testkeyfornow'
api = Api(app)

@app.before_first_request
def create_database():
    db.create_all()

jwt = JWT(app, authenticate, identity)

@jwt.auth_response_handler
def format_response(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'username': identity.username,
        'is_admin': identity.is_admin
    })

api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<int:id>')
api.add_resource(UserPasswordReset, '/reset/<int:id>')
api.add_resource(UserRegister, '/register')
api.add_resource(ShiftList, '/shifts')
api.add_resource(Shift, '/shift/<int:id>')
api.add_resource(ShiftClockIn, '/shift/<int:id>/clockin')
api.add_resource(ShiftClockOut, '/shift/<int:id>/clockout')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)