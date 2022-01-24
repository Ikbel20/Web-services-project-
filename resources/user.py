import sqlite3
from flask_restful import Resource, reqparse
from sqlalchemy.sql import select
from flask_jwt import jwt_required

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

    @jwt_required()
    def post(self,id):
        data=UserRegister.parser.parse_args()
        
        if UserModel.find_by_id(id):
            return{"message": "User with that id already exists."}, 400
        #user =  UserModel.query.filter_by(id=id).first()
        
        #user.id = id
        #user.username = data['username']
       # user.password = data['password']
        user = UserModel(id,data['username'],data['password'])
        user.save_to_db()
        return{"message": "User created successfully."}, 201
