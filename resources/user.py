import sqlite3
from flask_restful import Resource, reqparse

import validators # for the email 
from werkzeug.security import generate_password_hash


import os,sys
dir_path=os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, 
os.pardir))
sys.path.insert(0, parent_dir_path)

from models.user import UserModel

        
class UserRegister(Resource):
    TABLE_NAME='users'
    
    parser = reqparse.RequestParser()
   # parser.add_argument('id', type=int, required= True, help="This field cannot be left blank!")
    parser.add_argument('username', type=str, required= True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required= True, help="This field cannot be left blank!")
    parser.add_argument('email', type=str, required= True, help="This field cannot be left blank!")

 
    def post(self):
        data=UserRegister.parser.parse_args()
        
       
        if UserModel.find_by_username(data['username']):
            return{"error": "User with that name already exists."}, 409 # resource already exist
        if UserModel.find_by_email(data['email']):
            return{"message": "User with that email already exists."}, 409 


        #user =  UserModel.query.filter_by(id=id).first()
        if len(data['password'])<8:
             return{"Error": "Password is too short."}, 400 # Bad request
        if not data['username'].isalnum  or " " in data['username']:
            return{"Error": "Username should only contain letters or numbers "}, 400 # Bad request
        if not validators.email(data['email']):
             return{"Error": "Please enter a valid email  "}, 400 # Bad request
 
        user = UserModel(data['username'],data['password'],data['email'])
        pwd_hash= generate_password_hash(user.password)
        user.save_to_db()
        #return {'message':'gg'},201
        return {'message': 'user created successfully, here are the  coordinates {}'.format( user.json() )},201

    
    #def patch(self,id):



