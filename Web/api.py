from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db= SQLAlchemy(app)
api= Api(app)

class UserModel(db.Model):
    
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80), unique=True, nullable=False)
     email = db.Column(db.String(80), unique=True, nullable=False)

def __repr__ (self):
      return f"User(name = {self.name}, email = {self.name})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

userFields = {
     'id':fields.Integer,
     'name':fields.String,
     'email':fields.String,
}

class Users(Resource):
     @marshal_with(userFields)
     def get(self):
          Users = UserModel.query.all()
          return Users
     @marshal_with(userFields)
     def post(self):
          args = user_args.parse_args()
          user = UserModel(name=args["name"],email=args["email"])
          db.session.add(user)
          db.session.commit()
          users = UserModel.query.all()
          return Users, 201

api.add_resource(Users, '/api/users/')


@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'
if __name__ == '__main__':
    app.run(debug=True)

